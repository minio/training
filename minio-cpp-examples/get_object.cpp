// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX - License - Identifier: Apache - 2.0 

// Modified by MinIO for training and curriculum purposes.

//snippet-start:[s3.cpp.get_object.inc]
#include <iostream>
#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>
#include <aws/s3/model/GetObjectRequest.h>
#include <fstream>
#include <awsdoc/s3/s3_examples.h>
//snippet-end:[s3.cpp.get_object.inc]

// This import is required to provide the access key and secret key to MinIO
#include <aws/core/auth/AWSCredentialsProvider.h>

/* ////////////////////////////////////////////////////////////////////////////
 * Purpose: Prints the beginning contents of a text file in a 
 * bucket in Amazon S3.
 * For an example of downloading an entire, larger object, see the s3-crt example.
 *
 * Prerequisites: The bucket that contains the text file.
 *
 * Inputs:
 * - objectKey: The name of the text file.
 * - fromBucket: The name of the bucket that contains the text file.
 * - region: The AWS Region for the bucket.
 *
 * Outputs: true if the contents of the text file were retrieved; 
 * otherwise, false.
 * ///////////////////////////////////////////////////////////////////////// */

 // snippet-start:[s3.cpp.get_object.code]
bool AwsDoc::S3::GetObject(const Aws::String& objectKey,
    const Aws::String& fromBucket, const Aws::String& region)
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

    // Prepare the GetObject request
    //
    // If the file is nested under a prefix, such as BUCKET/data/bigdata.json
    // Specify the full prefix as the objectKey

    Aws::S3::Model::GetObjectRequest object_request;
    object_request.SetBucket(fromBucket);
    object_request.SetKey(objectKey);

    // Capture the GetObject response

    Aws::S3::Model::GetObjectOutcome get_object_outcome = 
        s3_client.GetObject(object_request);

    if (get_object_outcome.IsSuccess())
    {
        auto& retrieved_file = get_object_outcome.GetResultWithOwnership().
            GetBody();

        // Print a beginning portion of the text file.
        std::cout << "Beginning of file contents:\n";
        char file_data[255] = { 0 };
        retrieved_file.getline(file_data, 254);
        std::cout << file_data << std::endl;

        return true;
    }
    else
    {
        auto err = get_object_outcome.GetError();
        std::cout << "Error: GetObject: " <<
            err.GetExceptionName() << ": " << err.GetMessage() << std::endl;

        return false;
    }
}

int main(int argc, char *argv[])
{
    Aws::SDKOptions options;
    Aws::InitAPI(options);
    {
        const Aws::String bucket_name = "training";
        const Aws::String object_name = (argc>1)? argv[1]:"my-file.txt";
        const Aws::String region = "";

        if (!AwsDoc::S3::GetObject(object_name, bucket_name, region))
        {
            return 1;
        }
    }
    Aws::ShutdownAPI(options);

    return 0;
}
// snippet-end:[s3.cpp.get_object.code]
