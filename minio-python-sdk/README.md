# MinIO Python SDK Examples

This material is intended for use alongside MinIO Curriculum and Training
initiatives. All files are tested using Python 3.9

# Descriptions

The following table describes each Python file and its intended function. 

| File                     | Description |
| :---                     | :---        |
| `client_constructor.py`  | Contains functions for creating the MinIO Client object. <br><br>The `minio_play_client()` function creates a client object connecting to the https://play.min.io deployment. This is a sandbox environment useful for quick interaction with MinIO core features. <br><br>The `minio_client()` function creates a client object connecting to a MinIO server running on localhost. You can change this to point at any MinIO service. |
| `list_objects.py`        | Lists objects in a bucket. Defaults to listing objects in the `training` bucket. |
| `get_object.py`          | Gets an object from a bucket. Defaults to retrieving the `my-file.txt` object from the `training` bucket. |
| `put_object.py`          | Writes an object to a bucket. Defaults to writing the `my-file.txt` file to `training/my-file.txt` |
| `remove_object.py`       | Removes an object from a bucket. Defaults to removing the `my-file.txt` file from the `training` bucket.|
| `make_bucket.py`         | Creates a new bucket. Defaults to creating buckets without locking enabled |
| `enable_versioning.py`   | Toggles versioning on a bucket. Goes from Off -> Enable <-> Suspended |
| `generate_presigned.py`  | Generates a presigned GET, DELETE, or PUT URL for operating on a bucket without using the SDK. Defaults to GET against the `my-file.txt` file in the `training` bucket. |
| `webhook-server.py`      | Simple HTTP server for use as a [Webhook Notification Target](https://docs.min.io/minio/baremetal/monitoring/bucket-notifications/publish-events-to-webhook.html#minio-bucket-notifications-publish-webhook) |
| `create_bucket_event.py` | Configures a new bucket event for the Webhook target. Defaults to the `training` bucket. |
| `s3_select.py`           | Performs a simple query on a CSV file. Currently built to use the New York City [Directory of Temporary Public Art](https://data.cityofnewyork.us/Recreation/Directory-of-Temporary-Public-Art/zhrf-jnt6) as `nyc_public_art.csv`. |





All files use `argparse` - use the --help flag to see all available arguments for each file. For example:

```shell
$ python list_objects.py --help

usage: list_objects.py [-h] [--bucket BUCKET] [--versions VERSIONS]

optional arguments:
  -h, --help           show this help message and exit
  --bucket BUCKET      The name of the bucket into which we write the object
  --versions VERSIONS  Specify True to retrieve object version IDs
```