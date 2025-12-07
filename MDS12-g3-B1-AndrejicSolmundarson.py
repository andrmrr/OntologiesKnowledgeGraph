from rdflib import Graph, RDF, RDFS, XSD, URIRef

# from rdflib.namespace import XSD

def create_T_box(tbox: Graph, url):
    # we keep track of our properties
    properties = []

    # Papers
    paper =  URIRef(base=url, value='paper')

    topic = URIRef(base=url, value='topic')
    covers = URIRef(base=url, value='covers')
    tbox.add((covers, RDFS.domain, paper))
    tbox.add((covers, RDFS.range, topic))
    properties.append(covers)

    # citation 
    cites = URIRef(base=url, value='cites')
    tbox.add((cites, RDFS.domain, paper))
    tbox.add((cites, RDFS.range, paper))
    properties.append(cites)

    # authors and papers
    author = URIRef(base=url, value='author')
    corresponding_author = URIRef(base=url, value='corresponding_author')
    writes = URIRef(base=url, value='writes')
    tbox.add((writes, RDFS.domain, author))
    tbox.add((writes, RDFS.range, paper))
    tbox.add((corresponding_author, RDFS.subPropertyOf, writes))
    properties.append(writes)
    properties.append(corresponding_author)

    # reviews
    reviews = URIRef(base=url, value='reviews')
    tbox.add((reviews, RDFS.domain, author))
    tbox.add((reviews, RDFS.range, paper))
    properties.append(reviews)

    # venues, workshops, conferences, editions
    venue =   URIRef(base=url, value='venue')
    workshop =   URIRef(base=url, value='workshop')
    conference = URIRef(base=url, value='conference')
    edition = URIRef(base=url, value='edition')

    # venue
    tbox.add((workshop, RDFS.subClassOf, venue))
    tbox.add((conference, RDFS.subClassOf, venue))

    # workshop and conference
    hosts = URIRef(base=url, value='hosts')
    ws_hosts = URIRef(base=url, value='ws_hosts')
    cf_hosts = URIRef(base=url, value='cf_hosts')
    
    tbox.add((ws_hosts, RDFS.subPropertyOf, hosts))
    tbox.add((cf_hosts, RDFS.subPropertyOf, hosts))

    tbox.add((cf_hosts, RDFS.domain, conference))
    tbox.add((ws_hosts, RDFS.domain, workshop))
    tbox.add((hosts, RDFS.domain, venue))
    tbox.add((hosts, RDFS.range, edition))

    properties.append(hosts)
    properties.append(ws_hosts)
    properties.append(cf_hosts)

    # city and time for edition
    city =    URIRef(base=url, value='city')
    held_in = URIRef(base=url, value='held_in')
    tbox.add((held_in, RDFS.domain, edition))
    tbox.add((held_in, RDFS.range, city))
    properties.append(held_in)

    # journal and volume
    journal = URIRef(base=url, value='journal')
    volume =  URIRef(base=url, value='volume')
    publishes = URIRef(base=url, value='publishes')
    tbox.add((publishes, RDFS.domain, journal))
    tbox.add((publishes, RDFS.range, volume))
    properties.append(publishes)

    # publication
    publication = URIRef(base=url, value='publication')
    tbox.add((edition, RDFS.subClassOf, publication))
    tbox.add((volume, RDFS.subClassOf, publication))

    # volume, edition and publication
    published_in = URIRef(base=url, value='published_in')
    published_in_volume = URIRef(base=url, value='published_in_volume')
    published_in_edition = URIRef(base=url, value='published_in_edition')
    tbox.add((published_in_volume, RDFS.subPropertyOf, published_in))
    tbox.add((published_in_edition, RDFS.subPropertyOf, published_in))

    tbox.add((published_in, RDFS.domain, paper))
    tbox.add((published_in, RDFS.range, publication))
    tbox.add((published_in_volume, RDFS.range, volume))
    tbox.add((published_in_edition, RDFS.range, edition))

    properties.append(published_in)
    properties.append(published_in_edition)
    properties.append(published_in_volume)

    # Communities and Forums
    forum = URIRef(base=url, value='forum')

    tbox.add((venue, RDFS.subClassOf, forum))
    tbox.add((journal, RDFS.subClassOf, forum))

    community = URIRef(base=url, value='community')

    is_related_to_topic = URIRef(base=url, value='is_related_to_topic')
    is_related_to_community = URIRef(base=url, value='is_related_to_community')

    tbox.add((is_related_to_topic, RDFS.domain, community))
    tbox.add((is_related_to_topic, RDFS.range, topic))
    tbox.add((is_related_to_community, RDFS.domain, forum))
    tbox.add((is_related_to_community, RDFS.range, community))

    properties.append(is_related_to_community)
    properties.append(is_related_to_topic)


    # Add literals to the objects in the tbox
    # This is done by creating a property and setting the range to be a xsd data type

    # paper literals
    paper_key = URIRef(base=url, value='paper_key')
    tbox.add((paper_key, RDFS.domain, paper))
    tbox.add((paper_key, RDFS.range, XSD.string))
    properties.append(paper_key)

    paper_title = URIRef(base=url, value='paper_title')
    tbox.add((paper_title, RDFS.domain, paper))
    tbox.add((paper_title, RDFS.range, XSD.string))
    properties.append(paper_title)

    abstract = URIRef(base=url, value='abstract')
    tbox.add((abstract, RDFS.domain, paper))
    tbox.add((abstract, RDFS.range, XSD.string))
    properties.append(abstract)


    # topic literals
    topic_name = URIRef(base=url, value='topic_name')
    tbox.add((topic_name, RDFS.domain, topic))
    tbox.add((topic_name, RDFS.range, XSD.string))
    properties.append(topic_name)

    # author literals
    author_name = URIRef(base=url, value='author_name')
    tbox.add((author_name, RDFS.domain, author))
    tbox.add((author_name, RDFS.range, XSD.string))
    properties.append(author_name)

    # forum literals
    # it is enough to set the the name on the super class that way the 
    # subclasses journal and venue (workshop and conference) should inherit the property
    forum_name =   URIRef(base=url, value='forum_name')
    tbox.add((forum_name, RDFS.domain, forum))
    tbox.add((forum_name, RDFS.range, XSD.string))
    properties.append(forum_name)

    # community literals
    community_name = URIRef(base=url, value='community_name')
    tbox.add((community_name, RDFS.domain, community))
    tbox.add((community_name, RDFS.range, XSD.string))
    properties.append(community_name)

    # edition literals
    # year is saved a publication (superClass) property

    edition_title = URIRef(base=url, value='edition_title')
    tbox.add((edition_title, RDFS.domain, edition))
    tbox.add((edition_title, RDFS.range, XSD.string))
    properties.append(edition_title)

    # venue (workshop and conference) literals
    # defined with the superclass: forum

    # city literals
    city_name = URIRef(base=url, value='city_name') # TODO
    tbox.add((city_name, RDFS.domain, city))
    tbox.add((city_name, RDFS.range, XSD.string))
    properties.append(city_name)

    # journal literals
    # defined with the superclass forum

    # volume literals
    volume_title = URIRef(base=url, value='volume_title')
    tbox.add((volume_title, RDFS.domain, volume))
    tbox.add((volume_title, RDFS.range, XSD.string))
    properties.append(volume_title)
    
    # year is saved a publication (superClass) property
    
    volume_number = URIRef(base=url, value='volume_number')
    tbox.add((volume_number, RDFS.domain, volume))
    tbox.add((volume_number, RDFS.range, XSD.string))
    properties.append(volume_number)

    # publication literals
    pub_year = URIRef(base=url, value='pub_year')
    tbox.add((pub_year, RDFS.domain, publication))
    tbox.add((pub_year, RDFS.range, XSD.gYear))
    properties.append(pub_year)

    # add RDFS.Property type for every property
    for p in properties:
        tbox.add((p, RDF.type, RDF.Property))

    # this dictionary will be used to efficiently reference the TBOX when connecting the ABOX 
    # and the TBOX in the final ontology creation
    metas = {
        "paper": paper, 
        "author": author, 
        "journal": journal, 
        "volume": volume, 
        "topic": topic, 
        "edition": edition, 
        "conference": conference, 
        "workshop": workshop, 
        "abstract": abstract, 
        "city": city,
        "venue": venue, 
        "publication": publication,
        "forum": forum,
        "community": community,
        "covers": covers, 
        "cites": cites, 
        "city_name": city_name,
        "writes": writes, 
        "corresponding_author": corresponding_author, 
        "reviews": reviews, 
        "hosts": hosts, 
        "ws_hosts": ws_hosts, 
        "cf_hosts": cf_hosts, 
        "held_in": held_in, 
        "publishes": publishes, 
        "published_in": published_in, 
        "published_in_volume": published_in_volume, 
        "published_in_edition": published_in_edition, 
        "paper_key": paper_key, 
        "paper_title": paper_title,
        "abstract": abstract,
        "topic_name": topic_name,
        "author_name": author_name,
        "journal_title": forum_name,
        "volume_title": volume_title,
        "volume_number": volume_number,
        "volume_year": pub_year,
        "edition_year": pub_year, # overloading pub_year to use superclass properly
        "edition_title": edition_title,
        "workshop_name": forum_name, 
        "conference_name": forum_name, # overloading venue_name to use superclass properly
        # "pub_year": pub_year,
        "community_name": community_name,
        "is_related_to_topic": is_related_to_topic,
        "is_related_to_community": is_related_to_community
    }

    return tbox, metas

if __name__ == "__main__":
    # Our url for the project
    url = 'http://fib.upc.edu/sdm/2024/MDS12-g3/'
    g = Graph()
    g, metas = create_T_box(g, url)
    g.serialize("./tbox.ttl", format="turtle")
    print("T-Box created successfully!")