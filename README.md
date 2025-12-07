# Knowledge Graph Ontology for Academic Publications

The goal of this project is an **ontology** for analysis of academic publications using **RDFS** for data storage and processing. The project was done using **RDFS** library in **Python**. The project was an assignment for Semantic Data Management master's course conducted in a two people team. Further details about the assignment can be found in *Assignment.pdf*. The project includes creation of the ontology and its corresponding **SPARQL** queries.

## Instructions
### Export data command from Property Graph in neo4j v5:
CALL apoc.export.xls.all("property_graphs2.xls",{})

### Tbox
 - To create the tbox, run create_T_box.py > <output_file>

### Abox
 - To create the tbox and abox, run create_A_box.py > <output_file>

 ### Run the queries
 - To run a specific query and print the result, run queries.py -num <query_num (1-6)>
 - To run all queries and save the results in the /queries folder, run queries.py -all
