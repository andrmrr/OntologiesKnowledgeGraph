import pandas as pd
from rdflib import Graph, URIRef, Literal, RDF, RDFS

import warnings
warnings.filterwarnings("ignore")

# We require this funky way to import because of hyphens in the required naming convention
import importlib.util
# Create a module spec
spec = importlib.util.spec_from_file_location("partB1", f"MDS12-g3-B1-AndrejicSolmundarson.py")
# Load the module
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
create_T_box = module.create_T_box

def create_A_box(g: Graph, metas, url, file_path):
    # Read the Excel file
    xls = pd.ExcelFile(file_path)
    # define sheet names of the nodes
    all_nodes = {
        "paper": "Article", 
        "author": "Author", 
        "journal": "Journal", 
        "volume": "Volume", 
        "topic": "Topic", 
        "edition": "Event", 
        "conference": "Conference",
        "community": "Community"
    }
    # define sheet names of relationships
    all_relationship = {
        "covers": "IS_ABOUT", 
        "published_in": "PUBLISHED_IN", 
        "cites": "CITES", 
        "reviews": "REVIEWED_BY", 
        "part_of": "PART_OF", 
        "is_related_to_topic": "IS_RELATED",
        "is_related_to_community": "RELATED_TO_COMMUNITY"
        # "writes": "AUTHORED_BY" # remove this from the for loop because it requires extra steps
    }

    # dict to map the node id to the URI for creating the relationships. 
    id_to_uri = {} 

    # Add nodes
    for key, sheet_name in all_nodes.items(): # key is the node label, sheet_name is corresponding sheet in xls
        print(f"Adding {key} to abox")
        df = pd.read_excel(xls, sheet_name)
        # get the attributes of the nodes
        columns = df.columns.values[1:]
        meta = metas[key]

        for _, row in df.iterrows():
            # Create a URI for the node and keep for generating relationships
            node_uri = URIRef(base=url, value=f"{key}_{row[0]}")
            id_to_uri[row[0]] = node_uri

            # This shouldn't be needed but for some reason GraphDB requires it
            g.add((node_uri, RDF.type, meta))

            if key == 'paper': 
                # add abstract
                g.add((node_uri, metas["abstract"], Literal("this is an example abstract")))
            elif key == 'edition': 
                # add city
                city_name = "New York" if row[-1] >= 2015 else "Sydney"
                city = URIRef(base=url, value=f"city_{city_name.replace(' ', '_').upper()}") 
                g.add((node_uri, metas["held_in"], city))
                g.add((city, metas["city_name"], Literal(city_name)))

            # add attributes for the nodes
            for column in columns:
                try: 
                    g.add((node_uri, metas[f"{key}_{column}"], Literal(row[column])))
                except KeyError:
                    # properties not defined in the tbox will generate a key error and will not 
                    # be included in the abox. 
                    continue

    # Add relationships
    for key, sheet_name in all_relationship.items():# key is the property name, sheet_name is corresponding sheet in xls
        print(f"Adding {key} to abox")
        df = pd.read_excel(xls, sheet_name)
        
        # get the URI for the property
        meta = metas.get(key)
        for _, row in df.iterrows(): 
            source_id = row["<startNodeId>"]
            target_id = row["<endNodeId>"]
            
            source_uri = id_to_uri.get(source_id)
            target_uri = id_to_uri.get(target_id)
                
            if source_uri and target_uri:
                if key == "published_in":
                    if "volume" in target_uri:
                        meta = metas["published_in_volume"]
                    elif "edition" in target_uri:
                        meta = metas["published_in_edition"]
                    else:
                        raise Exception("Invalid target_uri for published_in relationship")
                elif key == "part_of":
                    tmp = source_uri
                    source_uri = target_uri
                    target_uri = tmp
                    if "conference" in source_uri:
                        meta = metas["cf_hosts"]
                    elif "workshop" in source_uri:
                        # we do not actually have workshops in the data but this would create them
                        # correctly
                        meta = metas["ws_hosts"]
                    elif "journal" in source_uri:
                        meta = metas["publishes"]
                    else:
                        raise Exception("Invalid source_uri for part_of relationship")
                elif key == "reviews":
                    tmp = source_uri
                    source_uri = target_uri
                    target_uri = tmp
                        
                g.add((source_uri, meta, target_uri))

    # Add writes and corresponding author
    print("Adding writes to abox")
    papers_with_corr_author = set()
    df = pd.read_excel(xls, "AUTHORED_BY")
    for _, row in df.iterrows(): 
        # the nodes are reversed in the property graph. 
        target_id = row["<startNodeId>"]
        source_id = row["<endNodeId>"]
        
        source_uri = id_to_uri.get(source_id)
        target_uri = id_to_uri.get(target_id)

        # check if the paper (target) already has a corresponding author
        meta = metas["writes"]
        if target_id not in papers_with_corr_author: 
            papers_with_corr_author.add(target_id)
            meta = metas["corresponding_author"]
        g.add((source_uri, meta, target_uri))

    return g


if __name__ == "__main__":
    file_path = "./property_graphs2.xls"
    url = "http://fib.upc.edu/sdm/2024/MDS12-g3/"
    g = Graph()
    g, metas = create_T_box(g, url)
    create_A_box(g, metas, url, file_path)
    g.serialize("./MDS12-g3-B2-AndrejicSolmundarson.ttl", format="turtle")
    print("A-Box created successfully!")
