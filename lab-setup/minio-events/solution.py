from flask import Flask, request, jsonify
from minio import Minio

client = Minio('localhost:9050', access_key='minioadmin', secret_key='minioadmin', secure=False)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    payload = request.get_json()
    print(payload)
    stats = client.stat_object(payload['Records'][0]['s3']['bucket']['name'], payload['Records'][0]['s3']['object']['key'])
    print("{0} last modified {1}, type {2}".format(stats.object_name,stats.last_modified,stats.content_type))
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7203)
