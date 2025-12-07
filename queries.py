from rdflib import  Graph
from rdflib.plugins.sparql import prepareQuery

from create_T_box import *
from create_A_box import *

import sys
import os   
import argparse
          
query1 = prepareQuery("""
        PREFIX upc: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?x WHERE {?x rdf:type upc:author}
    """)

query2 = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX upc: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        select DISTINCT ?p where {
            ?s ?p ?o .
            ?s rdf:type upc:author
        } limit 100
    """)

# TODO Query 3           
query3 = prepareQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ns1: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        SELECT ?x WHERE {
            {?x rdfs:domain ns1:journal} UNION {?x rdfs:domain ns1:conference}
        }
    """)

query4 = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX upc: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        select ?author where {
            ?author upc:writes ?paper .
            ?paper upc:published_in_edition ?e .
            ?conf upc:cf_hosts ?e .
            ?conf upc:is_related_to_community ?com .
            ?com upc:community_name "Database Community" .
        }
    """)

# TODO Custom Query          
query5 = prepareQuery("""
        PREFIX ns1: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        SELECT ?x ?y WHERE {
            {?x ns1:reviews ?p}
            {?y ns1:writes ?p} 
            {?y ns1:reviews ?p1}
            {?x ns1:writes ?p1} 
        }
    """)

query6 = prepareQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX upc: <http://fib.upc.edu/sdm/2024/MDS12-g3/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?author where {
            ?author upc:writes ?paper .
            ?paper upc:published_in ?pub .
            ?pub upc:pub_year ?year 
            FILTER ( ?year < "2014"^^xsd:integer )
        } 
        GROUP BY ?author
        HAVING (COUNT(?paper) > 15)
    """)

queries = [query1, query2, query3, query4, query5, query6]

if __name__ == "__main__":

    # define the console arguments
    parser = argparse.ArgumentParser(description='Execute SPARQL queries.')
    parser.add_argument('-num', '-n', metavar='N', type=int, action='store', choices=range(1, 7),
                        help='The number of the query to execute')
    parser.add_argument('-all', action='store_true', help='Execute all queries and store the \
                        results in the /queries folder')
    
    args = parser.parse_args()
    # print(args.num)
    # print(args.all)


    # create the graph
    file_path = "./property_graphs2.xls"
    url = "http://fib.upc.edu/sdm/2024/MDS12-g3/"

    g = Graph()
    g, metas = create_T_box(g, url)
    g = create_A_box(g, metas, url, file_path)

    if args.num is not None:
        if args.num == 1:
            query = query1
        elif args.num == 2:
            query = query2
        elif args.num == 3:
            query = query3
        elif args.num == 4:
            query = query4
        elif args.num == 5:
            query = query5
        elif args.num == 6:
            query = query6
        else:
            raise Exception("Invalid query number")
  
        results = g.query(query)
        for row in results:
            print(row[0])

    if args.all:
        if not os.path.exists("queries"):
            os.makedirs("queries")
        for i in range(len(queries)):
            q = queries[i]
            results = g.query(q)
            with open(f"queries/query{i+1}.txt", "w") as f:
                for row in results:
                    f.write(row[0] + "\n")
