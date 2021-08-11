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
    parser.add_argument("--versions", help="Specify True to retrieve object version IDs")

    args = parser.parse_args()

    # Populate the core arguments for list_objects

    bucket_name = args.bucket if args.bucket else "training"
    versions = args.versions if args.versions else False

    if versions:
        try:
            result = client.list_objects(
                bucket_name=bucket_name,
                include_version=True
            )

            print("Listing versioned objects for bucket {0}".format(bucket_name))

            for obj in result:
                # obj.version_id is the unique version ID for each object
                # obj.is_delete_marker returns True if this is a DeleteMarker tombstone
                # obj.is_latest returns True if this is the latest version of the object
                # You can find a defintion for the Object type in minio/datatypes.py -> class Object

                print("  Name: {0}\n  Size: {1}\n  Version ID: {2}\n  Delete Marker: {3}\n  Latest: {4}\n".
                    format(obj.object_name, obj.size, obj.version_id, obj.is_delete_marker, obj.is_latest))

        except S3Error as err:
            print("Error on writing object: \n\t{0}".format(err))

    elif not versions:
        try:
            result = client.list_objects(
                bucket_name=bucket_name
            )

            print("Listing objects for bucket {0}".format(bucket_name))

            for obj in result:
                print("  Name: {0}\n  Size: {1}\n".
                    format(obj.object_name, obj.size))

        except S3Error as err:
            print("Error on writing object: \n\t{0}".format(err))


if __name__ == '__main__':
    main()