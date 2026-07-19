# Smart Meter Electricity Consumption Data Pipeline
## Project Overview
This project implements an end-to-end Smart Meter Electricity Consumption Data Pipeline using PySpark, Delta Lake, and Databricks. The pipeline processes raw smart meter readings, performs data cleaning and validation, generates analytical datasets, detects abnormal electricity usage patterns, and enables SQL-based reporting.
The project follows the Medallion Architecture (Bronze → Silver → Gold) to ensure scalable and reliable data processing.
## Technologies Used
- Python
- PySpark
- Delta Lake
- Databricks
- Spark SQL
## Project Architecture
```
Raw CSV Data
      │
      ▼
Bronze Layer
(Data Ingestion)
      │
      ▼
Silver Layer
(Data Cleaning & Validation)
      │
      ▼
Gold Layer
(Aggregation & Analytics)
      │
      ▼
Anomaly Detection
      │
      ▼
SQL Analysis

##  Repository Structure
```
```
Smart_Meter_Data_Pipeline/
│
├── README.md
│
├── notebooks/
│   ├── 01_Bronze_Ingestion.html
│   ├── 02_Silver_Transformation.html
│   ├── 03_Gold_Aggregation.html
│   ├── 04_Anomaly_Detection.html
│   └── 05_SQL_Analysis.html
│
├── data/
│   ├── meter_readings.csv
│   └── household_info.csv
│
├── screenshots/
│   ├── 01_bronze_output.png
│   ├── 02_silver_output.png
│   ├── 03_gold_output.png
│   ├── 04_anomaly_output.png
│   └── 05_sql_output.png
```

---

## Pipeline Stages

### 1. Bronze Layer
- Ingest raw CSV files into Delta tables.
- Preserve raw data.
- Add ingestion timestamp for tracking.

### 2. Silver Layer
- Remove duplicate records.
- Validate electricity consumption values.
- Enrich data with household information.
- Create cleaned Delta tables.

### 3. Gold Layer
Generate business-ready datasets:
- Hourly Consumption
- Daily Consumption
- Monthly Consumption
- 7-Day Moving Average (SMA)

### 4. Anomaly Detection
Identify abnormal electricity consumption using:
- Spike Detection
- Zero Consumption Detection
- Usage Deviation Detection

Each detected anomaly includes:
- Expected Value
- Deviation Percentage
- Severity Level

### 5. SQL Analysis
Perform SQL-based analytics on Gold Layer tables to generate business insights and reports.

---

##  Output Tables

The project creates the following Delta tables:

### Bronze
- bronze_meter_readings

### Silver
- silver_meter_readings

### Gold
- gold_hourly_consumption
- gold_daily_consumption
- gold_monthly_consumption
- gold_prediction
- gold_anomaly_alerts

---

## Sample Outputs

Screenshots demonstrating each stage of the pipeline are available in the **screenshots/** folder.

- Bronze Output
- Silver Output
- Gold Aggregation
- Anomaly Detection
- SQL Analysis

---
