# coding: utf-8

from flask import Flask, request, jsonify, make_response
import random
import time

app = Flask(__name__)
app.config.update({"DEBUG": True})

MIN_PRICE = 1
MAX_PRICE = 100
MAX_SLEEP_TIME = 0.12

@app.route("/req", methods=["POST"])
def req():
    # SSPからリクエストを受信
    params = request.json
    request_id = request.json.get("request_id")
    app_id = request.json.get("app_id")
    url = "http://example.com/ad/image/" + str(app_id)
    price = random.randint(MIN_PRICE, MAX_PRICE)
    time.sleep(random.uniform(0, MAX_SLEEP_TIME))

    # SSPにレスポンスを送信
    response = {
        "request_id": request_id,
        "url": url,
        "price": price
    }
    return make_response(jsonify(response))


@app.route("/win", methods=["POST"])
def win():
    # SSPからリクエストを受信
    params = request.json
    request_id = request.json.get("request_id")
    price = request.json.get("price")
    time.sleep(random.uniform(0, MAX_SLEEP_TIME))

    # SSPにレスポンスを送信
    response = {
        "result": "ok"
    }
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(threaded=True, port=6000)
