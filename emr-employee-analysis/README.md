# 🏢 Employee Salary Analysis: 1 Billion Rows with PySpark on AWS EMR

## 📌 Project Overview
This project sets up an **Apache Spark job** on **AWS EMR** to find the **youngest active employee with the highest salary** among **1 billion employees** stored in Amazon S3. The dataset must be uploaded to **Amazon S3** before analysis.

The project consists of:
- **`calculate_salary.py`**: A PySpark script that reads a **Parquet** dataset from S3, processes it, and writes the aggregated results back to S3 in **CSV format**.
- **`EMRClusterEmployees.yaml`**: A CloudFormation template to launch an **AWS EMR cluster** with Spark installed and an automated Spark job step.

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
    --stack-name emr-cluster-employees \
    --template-body file://EMRClusterEmployees.yaml \
    --capabilities CAPABILITY_NAMED_IAM
```

📌 **Ensure** that you have the required IAM roles (`EMR_EC2_DefaultRole` and `EMR_DefaultRole`) created in your AWS account.

---

### **3️⃣ Run the PySpark Job on EMR**
Once the cluster is running, the PySpark job will automatically start. To submit the job manually:

```sh
aws emr add-steps \
    --cluster-id <your-cluster-id> \
    --steps '[{"Type":"Spark","Name":"Employee Salary Calculation","ActionOnFailure":"CONTINUE","Args":["spark-submit","s3://employees-large-code/calculate_salary.py","--input_uri","s3://employees-large/","--output_uri","s3://employees-large/output"]}]'
```

📌 Replace `<your-cluster-id>` with the actual EMR cluster ID.

---

### **4️⃣ Download the Result**
After the job is done, you can **download and print the result** using the following command:

```sh
aws s3 cp s3://<your-bucket>/output ./output --recursive --exclude "*" --include "*.csv" && cat ./output/*.csv
```

#### **📌 Example Console Output:**
```sh
id,name,age,salary,is_active
60326071,Alice,24,150000.0,true
```

📌 **Replace `<your-bucket>`** with your actual S3 bucket name before running the command.

---

## 📝 PySpark Script Details (`calculate_salary.py`)
This script:
1. **Loads an employee dataset from S3 (Parquet format).**
2. **Filters for active employees.**
3. **Finds the youngest employee with the highest salary.**
4. **Saves the results back to S3 in CSV format.**

### **Usage:**
```sh
python calculate_salary.py --input_uri s3://employees-large/ --output_uri s3://employees-large/output
```

---

## 📜 CloudFormation Template (`EMRClusterEmployees.yaml`)
This YAML file defines an **AWS EMR cluster** with:
- **Spark pre-installed**
- **1 master node (`m5.xlarge`)**
- **2 core nodes (`m5.xlarge`)**
- **Auto-termination after 60 seconds of inactivity**
- **Logs stored in S3**
- **A predefined EMR step to automatically run the salary calculation script**

### **Launch Manually via AWS CLI:**
```sh
aws cloudformation create-stack \
    --stack-name emr-cluster-employees \
    --template-body file://EMRClusterEmployees.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --on-failure DELETE
```

---

## 🗑️ Deleting the Stack
To tear down the EMR cluster and all associated resources:
```sh
aws cloudformation delete-stack --stack-name emr-cluster-employees
```

---

## 📌 Notes
- Ensure you have the necessary AWS permissions.
- Modify the `Ec2KeyName` in the CloudFormation template to your actual key pair.
- The output CSV files will be stored in `s3://employees-large/output`.

---

## 📧 Contact
For any issues, feel free to reach out or open a GitHub issue. 🚀