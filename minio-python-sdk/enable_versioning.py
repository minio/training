from minio.versioningconfig import VersioningConfig
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

    args = parser.parse_args()

    # Populate the core requirement for get_bucket_versioning and set_bucket_versioning

    bucket_name = args.bucket if args.bucket else "training"

    if not client.bucket_exists(bucket_name):        
        print("Bucket {0} does not exist on {1}".format(bucket_name, client._base_url.host))
        return

    # Grab the current bucket versioning status. 

    version_status = client.get_bucket_versioning(bucket_name).status
    print("Current versioning status of bucket {0} is {1}".format(bucket_name, version_status))

    # Toggle between states depending on versioning status:
    #   Off -> Enabled
    #   Enabled -> Suspended
    #   Suspended -> Enabled

    if version_status == "Off":
        try:
            print("Enabling versioning on bucket")
            client.set_bucket_versioning(bucket_name, VersioningConfig("Enabled"))
        except S3Error as err:
            print("Error on enabling versioning on bucket: \n\t{0}".format(err))
    
    elif version_status == "Enabled":
        try:
            print("Suspending versioning on bucket")
            client.set_bucket_versioning(bucket_name, VersioningConfig("Suspended"))
        except S3Error as err:
            print("Error on suspending versioning on bucket: \n\t{0}".format(err))

    elif version_status == "Suspended":
        try:
            print("Re-enabling versioning on bucket")
            client.set_bucket_versioning(bucket_name, VersioningConfig("Enabled"))
        except S3Error as err:
            print("Error on enabling versioning on bucket: \n\t{0}".format(err))

if __name__ == '__main__':
    main()