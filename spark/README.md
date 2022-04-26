# Spark and MinIO Training

These examples assume the following:

- Spark 3.2.x Coordinator and Worker
- hadoop-aws:3.2.x and aws-java-sdk-bundle dependency in Spark `jars/` path
- A MinIO deployment with the `spark` and `spark-job-output` directories
- One or more files from the [NYC Taxi Data Set](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

You may need to change hostnames or dataset names if your local setup has differing file names or folder structures.

# General Guidelines

Run the jobs using `spark-select <job>.py` and monitor the output.

The jobs use the `s3a://` connector to pull in a CSV file and perform basic SQL queries on a table generated from that CSV.

You can try to do more interesting things depending on your comfort with Spark.

The goal of these tutorials is just to provide a very basic working example of read/write via S3A and MinIO Object Storage.

# Question?

This training material is intended for use with MinIO Training and Development. Questions outside of that program should be directed to our Community Slack board at http://slack.min.io


