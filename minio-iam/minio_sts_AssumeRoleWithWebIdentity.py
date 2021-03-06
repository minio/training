# -*- coding: utf-8 -*-
# MinIO Python Library for Amazon S3 Compatible Cloud Storage,
# (C) 2020 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json

import urllib3

from minio import Minio
from minio.credentials import WebIdentityProvider


def get_jwt(client_id, client_secret, idp_client_id, idp_endpoint):
    res = urllib3.PoolManager().request(
        "POST",
        idp_endpoint,
        fields={
            "username": client_id,
            "password": client_secret,
            "grant_type": "password",
            "client_id": idp_client_id,
            "client_secret": idp_client_secret,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        encode_multipart=False
    )

    return json.loads(res.data.decode('utf-8'))


# IDP endpoint.
idp_endpoint = "http://localhost:8080/auth/realms/minio/protocol/openid-connect/token"

# Client-ID to fetch JWT.
client_id = "externaluser"

# Client secret to fetch JWT.
client_secret = "externaluser123"

# Client-ID of MinIO service on IDP.
idp_client_id = "account"

idp_client_secret= "SECRET"

# STS endpoint usually point to MinIO server.
sts_endpoint = "http://localhost:9000/"


provider = WebIdentityProvider(
    lambda: get_jwt(client_id, client_secret, idp_client_id, idp_endpoint),
    sts_endpoint,
)

client = Minio("localhost:9000", credentials=provider, secure=False)

# Get information of an object.
stat = client.stat_object("training", "Bird_raspberry.svg")
print(stat.object_name)
