import argparse
from minio.error import S3Error
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
    parser.add_argument("--bucket", help="The name of the bucket into which we write the object")
    parser.add_argument("--locking",help="Enable Bucking WORM Locking")

    args = parser.parse_args()

    # Populate the core requirements for make_bucket

    bucket_name = args.bucket if args.bucket else "training"
    locking = args.locking if args.locking else False

    # Use bucket_exists to see if the bucket already exists and exit if true

    if client.bucket_exists(bucket_name):
        print("Bucket {0} already exists on {1}".format(bucket_name, client._base_url.host))
        return

    try:
        if locking:
            client.make_bucket(bucket_name,object_lock=True)
            print("Created Bucket {0} with locking enabled".format(bucket_name))
        else:
            client.make_bucket(bucket_name)
            print("Created Bucket {0}".format(bucket_name))
    except S3Error as err:
        print("Error on creating bucket: \n\t{0}".format(err))
    
if __name__ == '__main__':
    main()