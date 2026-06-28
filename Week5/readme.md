# Week 5 - Apache Spark Assignment

# Assignment Overview
This assignment focuses on Apache Spark fundamentals, including DataFrame transformations, data cleaning, aggregations, filtering, schema handling, and processing pipelines using PySpark.

# Dataset Used
The assignment was implemented using the **Sample Superstore Dataset**, which was also used in the previous assignment.

Since some questions required columns that were not available in the original dataset, additional columns were created from existing data or generated for demonstration purposes.

# Additional Columns Created

| New Column | Derived From / Purpose |
|------------|------------------------|
| user_id | Customer ID |
| transaction_date | Order Date |
| product_category | Category |
| sale_amount | Sales |
| price | Sales |
| status | Created to demonstrate null value handling |
| age | Generated sample values for filtering operations |
| subscription | Generated sample values (Basic/Premium) |
| email | Generated from Customer Name |
| username | Generated from Customer Name |
| raw_timestamp | Derived from Order Date |
| event_time | Created by casting raw_timestamp to TimestampType |
| store_id | Derived from Region |

# Tasks Performed

- Compared Apache Spark with Hadoop MapReduce.
- Explained Spark's lazy evaluation and execution model.
- Removed duplicate records.
- Grouped and aggregated data.
- Handled missing (null) values.
- Counted records by category.
- Filtered records using multiple conditions.
- Converted date columns to TimestampType.
- Explained Shuffle and Wide Transformations.
- Cleaned datasets using DataFrame operations.
- Calculated multiple aggregations using `.agg()`.
- Built a complete Spark processing pipeline.

# Technologies Used

- Apache Spark
- PySpark
- Databricks Community Edition
- Python
- Sample Superstore Dataset

