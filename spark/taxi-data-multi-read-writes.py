from pyspark.sql import SparkSession
from pyspark import SparkConf

conf = SparkConf()

conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.3')
conf.set('spark.hadoop.fs.s3a.endpoint' , 'http://127.0.0.1:9000')
conf.set('spark.hadoop.fs.s3a.access.key', 'minioadmin')
conf.set('spark.hadoop.fs.s3a.secret.key','minioadmin')
conf.set('spark.hadoop.fs.s3a.path.style.access','true')
conf.set('spark.hadoop.fs.s3a.ssl.enabled','false')
conf.set('spark.hadoop.fs.s3a.aws.credentials.provider','org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
conf.set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
conf.set('spark.hadoop.fs.s3a.committer.magic.enabled','true')
conf.set('spark.hadoop.fs.s3a.committer.name','magic')


spark = SparkSession.builder.config(conf=conf).getOrCreate()

# This is a basic read of an object stored on the configured S3 target
# It loads a csv file from the 'spark' bucket with the specified prefix and path
# By specifying a wildcard we can ready all of the csv files matching the wildcard
# prefix of `yellow_tripdata_2021-`

df = spark \
          .read \
          .option('header','true') \
          .csv('s3a://spark/yellow_tripdata_2021-*.csv')

df.createOrReplaceTempView("TAXI")

print("Number of rows: " + str(df.count()))

res = spark.sql("""
           SELECT
           tpep_pickup_datetime,
           tpep_dropoff_datetime,
           passenger_count,
           trip_distance,
           case
               when payment_type = '1' then 'Credit'
               when payment_type = '2' then 'Cash'
               when payment_type = '3' then 'No Charge'
               when payment_type = '4' then 'Dispute'
               when payment_type = '5' then 'Unknown'
               when payment_type = '6' then 'Void'
           end as payment_type,
           tip_amount,
           total_amount
           FROM TAXI
        """)

res.show()

res \
    .coalesce(1) \
    .write.mode('overwrite') \
    .option('header','true') \
    .csv('s3a://spark-job-output/processed-taxi-data.csv')



