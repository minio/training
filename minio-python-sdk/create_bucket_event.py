from minio.notificationconfig import (NotificationConfig, QueueConfig)
from minio.error import S3Error
import argparse
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

    # Populate the core requirements for fputobject:

    bucket_name = args.bucket if args.bucket else "training"

    # We may need to change this webhook ARN depending on what MinIO lists as the available ARN
    # - MinIO Server outputs all configured ARNs on startup
    # - You can also get the ARN through the MinIO Console by checking the Settings
    #   and looking at the configured Notification Targets
    # - You can retrieve this at any time using a combination of mc and jq:
    #   $ mc admin info --json ALIAS | jq .info.sqsARN

    config = NotificationConfig(
        queue_config_list = [
            QueueConfig(
                "arn:minio:sqs::local:webhook",
                ["s3:ObjectCreated:*"],
                config_id="1"
            )
        ]
    )

    try:
        client.set_bucket_notification(bucket_name, config)
        
    except S3Error as err:
        print("Error on writing object: \n\t{0}".format(err))

if __name__ == '__main__':
    main()