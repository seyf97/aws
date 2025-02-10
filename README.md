# 🚀 Big Data Analytics with PySpark on AWS EMR

This repository contains two large-scale **Apache Spark** projects running on **AWS EMR**, processing large datasets efficiently.

## 📂 Projects
### **1️⃣ NY Taxi Fare Analysis (34M Rows)**  
- **Goal:** Calculate total taxi fares per vendor from NYC taxi trip records (34M+ rows).  
- **Dataset:** [NYC TLC Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) (Jan-Mar 2016).  
- **Key Tech:** PySpark, AWS EMR, AWS Cloudformation, Parquet, CSV.  
- **Project Directory:** [`emr-taxi-analysis/`](./emr-taxi-analysis/)  

### **2️⃣ Employee Salary Analysis (1B Rows)**  
- **Goal:** Find the youngest active employee with the highest salary from a dataset of randomly generated **1 billion records**.  
- **Dataset:** Employee salary records (stored in S3).  
- **Key Tech:** PySpark, AWS EMR, AWS Cloudformation, Parquet, Auto-termination.  
- **Project Directory:** [`emr-employee-analysis/`](./emr-employee-analysis/)  