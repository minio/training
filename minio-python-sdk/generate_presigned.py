import argparse
from minio.error import S3Error
from datetime import timedelta
from client_constructor import minio_client, minio_play_client

def main():

    # Example of client construction code:
    #
    # client = Minio(
    #     "play.min.io",
    #     access_key="minio",
    #     secret_key="minio123"
    # )

    client = minio_play_client()
    #client = minio_client()

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", help="The name of the bucket")
    parser.add_argument("--object_name",help="The name of the object")
    parser.add_argument("--http_action",help="Specify PUT for put, DELETE for delete, or GET for get. Defaults to GET")

    args = parser.parse_args()

    bucket_name = args.bucket if args.bucket else "training"
    object_name = args.object_name if args.object_name else "my-file.txt"
    http_action = args.http_action if args.http_action else "GET"

    if http_action == "GET":
        try:
            url = client.get_presigned_url(http_action, bucket_name, object_name, expires=timedelta(days=1))
            print("Presigned GET URL is {0}, expires in 7 days".format(url))
        except S3Error as err:
            print("Error generating presigned URL: \n\t{0}".format(err))

    elif http_action == "DELETE":
        try:
            url = client.get_presigned_url(http_action, bucket_name, object_name, expires=timedelta(days=1))
            print("Presigned DELETE URL is {0}, expires in 7 days".format(url))
        except S3Error as err:
            print("Error generating presigned URL: \n\t{0}".format(err))

    if http_action == "PUT":
        try:
            url = client.get_presigned_url(http_action, bucket_name, object_name, expires=timedelta(days=1),response_headers={"response-content-type":"application/json"})
            print("Presigned PUT URL is {0}, expires in 7 days".format(url))
        except S3Error as err:
            print("Error generating presigned URL: \n\t{0}".format(err))



if __name__ == '__main__':
    main()