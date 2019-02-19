# coding: utf-8

from flask import Flask, request, jsonify, make_response
import random


app = Flask(__name__)
app.config.update({"DEBUG": True })

@app.route("/req0", methods=["POST"])
@app.route("/req1", methods=["POST"])
@app.route("/req2", methods=["POST"])
@app.route("/req3", methods=["POST"])
@app.route("/req4", methods=["POST"])
def req():
    # SSPからリクエストを受信
    params = request.json
    request_id = request.json.get("request_id")
    app_id = request.json.get("app_id")
    url = "http://example.com/ad/image/" + str(app_id)
    price = random.randint(1,10) * 5

    # SSPにレスポンスを送信
    response = {}
    response["request_id"] = request_id
    response["url"] = url
    response["price"] = price
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run()
