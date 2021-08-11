import argparse
from minio.error import S3Error
from http.client import HTTPResponse
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
    parser.add_argument("--object_name",help="The name of the object")
    parser.add_argument("--version_id",help="The version ID of the object to get")

    args = parser.parse_args()

    # Populate the core requirements for getobject
    # Set version to empty string if we just want the "latest" version of the object

    bucket_name = args.bucket if args.bucket else "training"
    object_name = args.object_name if args.object_name else "my-file.txt"
    version_id = args.version_id if args.version_id else ""

    try:
        if not version_id:
            result = client.get_object(
                bucket_name=bucket_name,
                object_name=object_name
            )

            print("Contents of object {0}/{1}: \n  {2}".format(bucket_name, object_name,result.data.decode()[0:254]))
        else:
            result = client.get_object(
                bucket_name=bucket_name,
                object_name=object_name,
                version_id=version_id
            )

            print("Contents of object {0}/{1} with version {2}: \n  {3}".format(bucket_name, object_name,version_id,result.data.decode()[0:254]))
            
        result.close()
        result.release_conn()
        
    except S3Error as err:
        print("Error on retrieving object: \n\t{0}".format(err))

if __name__ == '__main__':
    main()
