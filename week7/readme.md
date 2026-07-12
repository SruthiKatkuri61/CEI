Week 7 - Delta Lake MERGE Implementation
Objective:
Perform incremental data processing using Delta Lake by applying the MERGE operation to update existing records and insert new records into a Delta table.
Assignment Overview:-
This project demonstrates the implementation of Delta Lake MERGE (UPSERT) using Databricks.
The workflow includes:
- Loading the master dataset into a Delta table
- Performing basic data cleaning
- Creating and loading an incremental dataset
- Applying the Delta Lake MERGE operation
- Validating the final results

Technologies Used
- Databricks Community Edition
- Apache Spark (PySpark)
- Delta Lake
- Python

 Dataset
Master Dataset
- customer_master.csv
- Total Records: 9,994
Incremental Dataset
- customer_incremental.csv
- Total Records: 300
