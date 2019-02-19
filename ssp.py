# coding: utf-8

from flask import Flask, request, jsonify, make_response
from datetime import datetime
import uuid
import requests
import json

app = Flask(__name__)
app.config.update({"DEBUG": True})

@app.route("/req", methods=["POST"])
def req():
    # SDKからリクエストを受信
    request_time = datetime.now().strftime("%Y%m%d-%H%M%S.%4N")
    app_id = request.json.get("app_id")
    ssp_name = "y_sako"
    request_id = ssp_name + "-" + str(uuid.uuid4())

    # DSPにリクエストを送信
    # url = "http://dsp1.example.jp/req"
    url = "http://localhost:5000/req"
    headers = {"content-type": "application/json"}
    payload = {
        "ssp_name": ssp_name,
        "request_time": request_time,
        "request_id": request_id,
        "app_id": app_id
    }
    dict = [(url+str(i), requests.post(url+str(i), json.dumps(payload), headers=headers).json().get("price")) for i in range(5)]

    # DSPからのレスポンスを集計
    dict.sort(key=lambda x: x[1], reverse=True)
    url = dict[0][0]
    price = dict[1][1]

    # SDKにレスポンスを送信
    response = {"url": url, "price": price}
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(port=4000)
