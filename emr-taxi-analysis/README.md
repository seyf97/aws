# 🚖 Taxi Fare Aggregation with PySpark on AWS EMR

## 📌 Project Overview
This project sets up an **Apache Spark job** on **AWS EMR** to calculate the total taxi fares per vendor from a given dataset stored in Amazon S3. The dataset is sourced from [NYC Taxi & Limousine Commission Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), covering the period from **January 2016 to March 2016 (3 months)** with over **34 million rows**. The dataset must be uploaded to **Amazon S3** for analysis. 

The project consists of:
- **`calculate_sum.py`**: A PySpark script that reads a **Parquet** dataset from S3, processes it, and writes the aggregated results back to S3 in **CSV format**.
- **`spark-emr-cluster.yaml`**: A CloudFormation template to launch an **AWS EMR cluster** with Spark installed.

---

## 🚀 Deployment Steps
### **1️⃣ Create Default EMR Roles**
Before launching the cluster, ensure that the required IAM roles exist by running:

```sh
aws emr create-default-roles
```

This command creates the necessary IAM roles: `EMR_EC2_DefaultRole` and `EMR_DefaultRole`.

---

### **2️⃣ Launch an EMR Cluster**
Use the provided **CloudFormation template** to deploy an **EMR 7.7.0** cluster with Spark:

```sh
aws cloudformation create-stack \
    --stack-name spark-emr-cluster \
    --template-body spark-emr-cluster.yaml \
    --capabilities CAPABILITY_NAMED_IAM
```

📌 **Ensure** that you have the required IAM roles (`EMR_EC2_DefaultRole` and `EMR_DefaultRole`) created in your AWS account.

---

### **3️⃣ Run the PySpark Job on EMR**
Once the cluster is running, submit the PySpark job to process the dataset:

```sh
aws emr add-steps \
    --cluster-id <your-cluster-id> \
    --steps 'Type=Spark,Name="Taxi Fare Aggregation",ActionOnFailure=CONTINUE,Args=[s3://taxi-project/calculate_sum.py,--input_uri,s3://taxi-project/trip_data.snappy.parquet,--output_uri,s3://taxi-project/output]'
```

📌 Replace `<your-cluster-id>` with the actual EMR cluster ID.

---

## 📝 PySpark Script Details (`calculate_sum.py`)
This script:
1. **Loads a taxi dataset from S3 (Parquet format).**
2. **Aggregates `total_amount` per `VendorID`.**
3. **Saves the results back to S3 in CSV format.**

### **Usage:**
```sh
python calculate_sum.py --input_uri s3://taxi-project/trip_data.snappy.parquet --output_uri s3://taxi-project/output
```

---

## 📜 CloudFormation Template (`spark-emr-cluster.yaml`)
This YAML file defines an **AWS EMR cluster** with:
- **Spark pre-installed**
- **1 master node (`m5.xlarge`)**
- **2 core nodes (`m5.xlarge`)**
- **Logs stored in S3**

### **Launch Manually via AWS CLI:**
```sh
aws cloudformation create-stack \
    --stack-name spark-emr-cluster \
    --template-body file://spark-emr-cluster.yaml \
    --capabilities CAPABILITY_NAMED_IAM
```

---

## 🗑️ Deleting the Stack
To tear down the EMR cluster and all associated resources:
```sh
aws cloudformation delete-stack --stack-name spark-emr-cluster
```

---

## 📌 Notes
- Ensure you have the necessary AWS permissions.
- Modify the `Ec2KeyName` in the CloudFormation template to your actual key pair.
- The output CSV files will be stored in `s3://taxi-project/output`.

---

## 📧 Contact
For any issues, feel free to reach out or open a GitHub issue. 🚀

