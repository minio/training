// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX - License - Identifier: Apache - 2.0 

// Modified by MinIO for training and curriculum purposes.

// snippet-start:[s3.cpp.delete_object.inc]
#include <iostream>
#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>
#include <aws/s3/model/DeleteObjectRequest.h>
#include <awsdoc/s3/s3_examples.h>
// snippet-end:[s3.cpp.delete_object.inc]

// This import is required to provide the access key and secret key to MinIO
#include <aws/core/auth/AWSCredentialsProvider.h>

/* ////////////////////////////////////////////////////////////////////////////
 * Purpose: Deletes an object from a bucket in Amazon S3.
 *
 * Prerequisites: The bucket containing the object to be deleted.
 *
 * Inputs:
 * - objectKey: The name of the object to delete.
 * - fromBucket: The name of the bucket to delete the object from.
 * - region: The AWS Region to create the bucket in.
 *
 * Outputs: true if the object was deleted; otherwise, false.
 * ///////////////////////////////////////////////////////////////////////// */

// snippet-start:[s3.cpp.delete_object.code]
bool AwsDoc::S3::DeleteObject(const Aws::String& objectKey, 
    const Aws::String& fromBucket,const Aws::String& region)
{
    Aws::Client::ClientConfiguration config;

    // This code is retained from the AWS implementation, 
    // but MinIO does not require nor rely on the region by default. 
    //
    // You only need to set region if the MinIO server is explicitly started with a region.
    // Otherwise you can just specify an empty string.
    

    if (!region.empty())
    {
        config.region = region;
    }

    // Override the endpoint to the MinIO deployment.
    // The following URL is a hosted MinIO instance at https://play.min.io
    // We need to both override the endpoint and set the HTTP scheme to HTTPS

    config.endpointOverride = "play.min.io:9000";
    config.scheme = Aws::Http::Scheme::HTTPS;


    // Initialize the client and point it at MinIO
    // Note that we set the AWSCredentials based on the credentials of a user on MinIO Play
    
    Aws::S3::S3Client s3_client(
                        Aws::Auth::AWSCredentials("Q3AM3UQ867SPQQA43P2F","zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"),
    			        config,
        				Aws::Client::AWSAuthV4Signer::PayloadSigningPolicy::Always,
		        		false
                        );

    // Prepare the DeleteObject Request
    //
    // If the file is nested under a prefix, such as BUCKET/data/bigdata.json
    // Specify the full prefix as the objectKey

    Aws::S3::Model::DeleteObjectRequest request;

    request.WithKey(objectKey)
        .WithBucket(fromBucket);

    Aws::S3::Model::DeleteObjectOutcome outcome = 
        s3_client.DeleteObject(request);

    if (!outcome.IsSuccess())
    {
        auto err = outcome.GetError();
        std::cout << "Error: DeleteObject: " 
                  << err.GetExceptionName() 
                  << ": " 
                  << err.GetMessage() 
                  << std::endl;

        return false;
    }
    else
    {
        return true;
    }
}

int main(int argc, char *argv[])
{
    const Aws::String from_bucket = "training";
    const Aws::String object_key = (argc>1)? argv[1]:"my-file.txt";
    const Aws::String region = "";

    Aws::SDKOptions options;
    Aws::InitAPI(options);
    {
        if (AwsDoc::S3::DeleteObject(object_key, from_bucket, region))
        {
            std::cout << "Deleted object " << object_key <<
                " from " << from_bucket << "." << std::endl;
        }
    }
    ShutdownAPI(options);

    return 0;
}
// snippet-end:[s3.cpp.delete_object.code]