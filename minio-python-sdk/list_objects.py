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
    parser.add_argument("--bucket",   help="The name of the bucket into which we write the object")
    parser.add_argument("--versions", help="Specify True to retrieve object version IDs")

    args = parser.parse_args()

    # Populate the core arguments for list_objects

    bucket_name = args.bucket or "training"
    versions    = args.versions or False

    try:
        result = client.list_objects(
            bucket_name=bucket_name,
            include_version=versions
        )

        print("Listing objects and directories in bucket {0} {1}".format(
            bucket_name,
            ("with versioning information") if versions else ""
        ))

        for obj in result:
            print("\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
                    "Object Name: " + obj.object_name + "\n",
                    "Object Size: " + str(obj.size) + "\n",
                    "Directory: " + str(obj.is_dir) + "\n",
                    ("Version ID: " + str(obj.version_id) + "\n") if versions else "",
                    ("Deleted: " + str(obj.is_delete_marker) + "\n") if versions else "",
                    ("Latest: " + str(obj.is_latest) + "\n") if versions else "",
                )
            )

    except S3Error as err:
        print("error")


if __name__ == '__main__':
    main()
