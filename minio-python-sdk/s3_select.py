from minio import Minio
import argparse
import sys
from minio.error import S3Error
from minio.select import SelectRequest, CSVInputSerialization, CSVOutputSerialization, SelectObjectReader, Stats

def main():

    client = Minio(
        "play.min.io",
        access_key="minio",
        secret_key="minio123"
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", help="The name of the bucket into which we write the object")
    parser.add_argument("--object_name",help="The name of the object")

    args = parser.parse_args()

    bucket_name = args.bucket if args.bucket else "training"
    object_name = args.object_name if args.object_name else "nyc_public_art.csv"

    try:
        with client.select_object_content(
                bucket_name, 
                object_name, 
                SelectRequest(
                    "select s.\"name\",s.\"artist\",s.\"active\" from S3Object s limit 10", 
                    CSVInputSerialization(file_header_info="USE"), 
                    CSVOutputSerialization(),
                    request_progress=True)
            ) as result:
                for data in result.stream():
                    print("name,artist,active")
                    print(data.decode())
                
                print(" Bytes Scanned: {0}\n Bytes Processed: {1}\n Bytes Returned: {2}".
                    format(result.stats().bytes_scanned, result.stats().bytes_processed, result.stats().bytes_returned))
    
    except S3Error as err:
        print("Error on running S3 Select Query: \n\t{0}".format(err))



if __name__ == '__main__':
    main()