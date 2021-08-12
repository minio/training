// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX - License - Identifier: Apache - 2.0 

#pragma once

#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>
#include <aws/s3/model/BucketLocationConstraint.h>
#include <awsdoc/s3/S3_EXPORTS.h>

namespace AwsDoc
{
    namespace S3
    {
        AWSDOC_S3_API bool CreateBucket(const Aws::String& bucketName, 
            const Aws::S3::Model::BucketLocationConstraint& region);
        AWSDOC_S3_API bool DeleteObject(const Aws::String& objectKey,
            const Aws::String& fromBucket, const Aws::String& region = "");
        AWSDOC_S3_API bool GetObject(const Aws::String& objectKey,
            const Aws::String& fromBucket, const Aws::String& region = "");
        AWSDOC_S3_API bool ListObjects(const Aws::String& bucketName, 
            const Aws::String& region = "");
        AWSDOC_S3_API bool PutObject(const Aws::String& bucketName,
            const Aws::String& objectName,
            const Aws::String& region = "");
    }
}
