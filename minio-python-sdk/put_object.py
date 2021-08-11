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
    parser.add_argument("--object_path",help="The path to the object. Specify a local or full filesystem path")
    parser.add_argument("--object_name",help="The name of the object")

    args = parser.parse_args()

    # Populate the core requirements for fputobject:

    bucket_name = args.bucket if args.bucket else "training"
    object_name = args.object_name if args.object_name else "my-file.txt"
    object_path = args.object_path if args.object_path else "my-file.txt"

    print("Writing object {0} to {1}/{2}".format(object_path, object_name, bucket_name))

    try:

        # Capture the result of writing the object to the bucket

        result = client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=object_path
        )

        print("Wrote object to: {0}/{1}".format(result.bucket_name,result.object_name))

    except S3Error as err:
        print("Error on writing object: \n\t{0}".format(err))

if __name__ == '__main__':
    main()