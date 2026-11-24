from flask import Flask, request, jsonify
from gateway import dispatch

app = Flask(__name__)


@app.route("/orders", methods=["POST"])
def create_order():
    body = request.get_json(silent=True) or {}
    which, result = dispatch(body)
    resp = jsonify(result)
    resp.headers["X-Order-Handler"] = which
    return resp, (201 if which == "v2" else 200)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
