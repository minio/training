from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    payload = request.get_json()
    print(payload)
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7203)
