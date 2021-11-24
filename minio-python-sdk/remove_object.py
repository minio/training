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
    parser.add_argument("--bucket",      help="The name of the bucket into which we write the object")
    parser.add_argument("--object_name", help="The name of the object")
    parser.add_argument("--version_id",  help="The version ID of the object to delete")

    args = parser.parse_args()

    # Populate the core requirements for remove_object
    # Set version_id to empty string to delete latest object by default

    bucket_name = args.bucket      or "training"
    object_name = args.object_name or "my-file.txt"
    version_id  = args.version_id  or ""

    try:
        client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name,
            version_id = version_id or None
        )

        print("Deleted object: {0}/{1} {2}".format(
            bucket_name,
            object_name,
            ("Wth version ID: " + version_id) if version_id else ""
        ))

    except S3Error as err:
        print("Error on removing object \n\t{0}".format(err))


if __name__ == '__main__':
    main()
