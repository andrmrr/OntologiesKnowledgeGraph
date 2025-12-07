# Knowledge Graph
## SDM Lab2

### Export data command from Property Graph in neo4j v5:
CALL apoc.export.xls.all("property_graphs2.xls",{})

### Tbox
 - To create the tbox, run create_T_box.py > <output_file>

### Abox
 - To create the tbox and abox, run create_A_box.py > <output_file>

 ### Run the queries
 - To run a specific query and print the result, run queries.py -num <query_num (1-6)>
 - To run all queries and save the results in the /queries folder, run queries.py -all