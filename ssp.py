# coding: utf-8

from flask import Flask, request, jsonify, make_response
from datetime import datetime
import uuid
import requests
import json
from joblib import Parallel, delayed

app = Flask(__name__)
app.config.update({"DEBUG": True})

def get_price(url, payload):
    headers = {"content-type": "application/json"}
    price = requests.post(url, json.dumps(payload), headers=headers).json().get("price")
    return (url, price)

@app.route("/req", methods=["POST"])
def req():
    # SDKからリクエストを受信
    now = datetime.now()
    request_time = now.strftime("%Y%m%d-%H%M%S.") + str(now.microsecond)[:4]
    app_id = request.json.get("app_id")
    ssp_name = "y_sako"
    request_id = ssp_name + "-" + str(uuid.uuid4())

    # DSPにリクエストを送信
    # url = "http://dsp1.example.jp/req"
    url = "http://localhost:5000/req"
    payload = {
        "ssp_name": ssp_name,
        "request_time": request_time,
        "request_id": request_id,
        "app_id": app_id
    }
    result = Parallel(n_jobs=-1)([delayed(get_price)(url+str(n), payload) for n in range(5)])

    # DSPからのレスポンスを集計
    result.sort(key=lambda x: x[1], reverse=True)
    url = result[0][0]
    price = result[1][1]

    # SDKにレスポンスを送信
    response = {"url": url, "price": price}
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(port=4000)
