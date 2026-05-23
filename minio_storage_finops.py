import os
import re
from dotenv import load_dotenv
import boto3
from botocore.client import Config
import csv
from collections import defaultdict

# Load variables from .env
load_dotenv()

endpoint_url = os.getenv('S3_ENDPOINT')
access_key = os.getenv('S3_ACCESS_KEY')
secret_key = os.getenv('S3_SECRET_KEY')
bucket_name = os.getenv('S3_BUCKET')

if not all([endpoint_url, access_key, secret_key, bucket_name]):
    raise EnvironmentError("❌ Missing required S3 environment variables in .env")

# Connect to MinIO/S3
s3 = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Prepare data structures
policy_sizes = defaultdict(int)
policy_counts = defaultdict(int)

# Regex to extract policy name
# Example: k10/93a0955b-.../migration/wordpress-backup/file.snap
policy_pattern = re.compile(r'k10/[^/]+/migration/([^/]+)/')

print(f"📦 Analyzing objects in bucket '{bucket_name}'...\n")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

total_objects = 0
total_size = 0

for page in pages:
    for obj in page.get('Contents', []):
        key = obj['Key']
        size = obj['Size']
        total_objects += 1
        total_size += size

        match = policy_pattern.search(key)
        if match:
            policy = match.group(1)
            policy_sizes[policy] += size
            policy_counts[policy] += 1

# Generate the CSV report
csv_file = 's3_policy_report.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Policy', 'Object Count', 'Total Size (bytes)', 'Total Size (GB)'])

    for policy in sorted(policy_sizes.keys()):
        size = policy_sizes[policy]
        count = policy_counts[policy]
        size_gb = size / (1024 ** 3)
        writer.writerow([policy, count, size, f"{size_gb:.2f}"])

# Console summary
print("📊 Storage usage per policy:\n")
for policy in sorted(policy_sizes.keys()):
    size = policy_sizes[policy]
    count = policy_counts[policy]
    print(f"• {policy:25} : {count:4} objects | {size:,} bytes (~{size / (1024**3):.2f} GB)")

print(f"\n✅ {total_objects} objects analyzed (total ~{total_size / (1024**3):.2f} GB)")
print(f"📄 Report generated: {csv_file}")
