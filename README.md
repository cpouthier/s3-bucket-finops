# 📊 MinIO S3 Policy Storage Report

This script is designed to **analyze object storage usage in a MinIO (or AWS S3-compatible) bucket** and generate a **per-policy storage report** in CSV format. It is especially useful for **FinOps, billing, and cleanup use cases**.

---

## ✅ Purpose

The script scans all objects in a given S3 bucket and:
- Identifies backup **policies** based on the folder structure  
  (e.g. `k10/<uuid>/migration/<policy-name>/...`)
- Calculates the **total number of objects** and **total size** for each policy
- Outputs the results as a **CSV report** and a **console summary**

---

## 📦 Prerequisites

- **Python 3.7+**
- The following Python packages (installed automatically via the provided `install_and_run.sh` script):
  - `boto3`
  - `python-dotenv`
- A `.env` file with the following environment variables:
  ```dotenv
  S3_ENDPOINT=http://your-minio-host:9000
  S3_ACCESS_KEY=your-access-key
  S3_SECRET_KEY=your-secret-key
  S3_BUCKET=your-bucket-name

You must have access to the bucket and permissions to list objects.

## 🚀 How It Works

1. The script uses `boto3` to connect to your MinIO/S3 instance using credentials and endpoint defined in the `.env` file.

2. It scans **all objects** in the specified bucket and filters those whose path matches the following structure:

k10/<uuid>/migration/<policy-name>/...

- Example object key:  
  `k10/93a0955b-df5a-42de-ac1f-8061385fa658/migration/wordpress-backup/file.snap`

3. It extracts the `<policy-name>` from the object path and:
- Counts how many objects are associated with each policy
- Sums the total storage size (in bytes and GB) for each policy

4. It writes a CSV report (`s3_policy_report.csv`) with the following columns:
- `Policy`
- `Object Count`
- `Total Size (bytes)`
- `Total Size (GB)`

5. It also prints a human-readable summary of storage usage per policy directly to the console.

## ▶️ How to Run

1. Make sure you have a `.env` file in the same directory with the following variables:

   ```dotenv
   S3_ENDPOINT=http://your-minio-host:9000
   S3_ACCESS_KEY=your-access-key
   S3_SECRET_KEY=your-secret-key
   S3_BUCKET=your-bucket-name

2. Run the provided setup and execution script:

chmod +x install_and_run.sh
./install_and_run.sh

This script will:

Create a Python virtual environment (.venv-s3) if it doesn't already exist
Install required dependencies (boto3 and python-dotenv)
Execute the report script: minio_storage_finops.py

3. After execution:
   The terminal will display a summary of storage usage per policy
A detailed CSV file named s3_policy_report.csv will be created in the current directory
