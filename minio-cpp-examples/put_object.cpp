// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX - License - Identifier: Apache - 2.0

// Modified by MinIO for training and curriculum purposes.

//snippet-start:[s3.cpp.put_object.inc]
#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>
#include <aws/s3/model/PutObjectRequest.h>
#include <awsdoc/s3/s3_examples.h>
//snippet-end:[s3.cpp.put_object.inc]

// This import is required to provide the access key and secret key to MinIO
#include <aws/core/auth/AWSCredentialsProvider.h>

/* ////////////////////////////////////////////////////////////////////////////
 * Purpose: Adds an object to an Amazon S3 bucket.
 * For an example of a multipart upload, see the s3-crt code example.
 *
 * Prerequisites: An Amazon S3 bucket and the object to be added.
 *
 * Inputs:
 * - bucketName: The name of the bucket.
 * - objectName: The name of the object.
 * - region: The AWS Region for the bucket.
 *
 * Outputs: true if the object was added to the bucket; otherwise, false.
 * ///////////////////////////////////////////////////////////////////////// */

// snippet-start:[s3.cpp.put_object.code]
bool AwsDoc::S3::PutObject(const Aws::String& bucketName, 
    const Aws::String& objectName,
    const Aws::String& region)
{
    // Verify that the file exists.
    struct stat buffer;

    if (stat(objectName.c_str(), &buffer) == -1)
    {
        std::cout << "Error: PutObject: File '" <<
            objectName << "' does not exist." << std::endl;

        return false;
    }

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


    // Prepare the PutObject request
    Aws::S3::Model::PutObjectRequest request;
    request.SetBucket(bucketName);

    // We are using the name of the file as the key for the object in the bucket.
    // However, this is just a string and can set according to your retrieval needs.
    // If you want to preserve filepaths, specify the full prefix as part of the object name.
    //
    // For example, "/data/bigdata.json" gets saved to MinIO with that full path prefix.
    // You would access that object through BUCKET/data/bigdata.json

    request.SetKey(objectName);

    // Prepare the object data from file

    std::shared_ptr<Aws::IOStream> input_data = 
        Aws::MakeShared<Aws::FStream>("SampleAllocationTag", 
            objectName.c_str(), 
            std::ios_base::in | std::ios_base::binary);

    request.SetBody(input_data);

    // Capture the outcome of the PutObject request.

    Aws::S3::Model::PutObjectOutcome outcome = 
        s3_client.PutObject(request);

    if (outcome.IsSuccess()) {

        std::cout << "Added object '" << objectName << "' to bucket '"
            << bucketName << "'.\n";
        return true;
    }
    else
    {
        std::cout << "Error: PutObject: " << 
            outcome.GetError().GetMessage() << std::endl;
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

        if (!AwsDoc::S3::PutObject(bucket_name, object_name, region)) {   
            return 1;
        }
    }
    Aws::ShutdownAPI(options);

    return 0;
}
// snippet-end:[s3.cpp.put_object.code]
