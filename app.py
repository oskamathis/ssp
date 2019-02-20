# coding: utf-8

from flask import Flask, request, jsonify, make_response
from datetime import datetime
from multiprocessing import Pool
from timeout_decorator import timeout, TimeoutError
import uuid
import requests
import json
import multiprocessing as multi
import random
import os

app = Flask(__name__)
config = json.load(open("config.json", "r"))

SSP_NAME = "y_sako"
HEADERS = {"content-type": "application/json"}
AD_URL = "http://example.com/ad/image/"
ENV = os.getenv("FLASK_APP_ENV", "production")

if ENV == "development":
    app.config.update({"DEBUG": True})

def process(args):
    try:
        return send_request(*args)
    except TimeoutError:
        return None

@timeout(0.1)
def send_request(url, payload):
    response = requests.post(url+"/req", json.dumps(payload), headers=HEADERS).json()
    ad_url = response.get("url")
    price = response.get("price")
    return (ad_url, price, url)


@app.route("/req", methods=["POST"])
def req():
    # SDKからリクエストを受信
    now = datetime.now()
    request_time = now.strftime("%Y%m%d-%H%M%S.") + str(now.microsecond)[:4]
    app_id = request.json.get("app_id")
    request_id = SSP_NAME + "-" + str(uuid.uuid4())

    # DSPにリクエストを送信
    urls = ("http://" + host + ":" + port for host, port in config[ENV]["DSP"])
    payload = {
        "ssp_name": SSP_NAME,
        "request_time": request_time,
        "request_id": request_id,
        "app_id": app_id
    }

    n_cores = multi.cpu_count()
    with Pool(n_cores) as pool:
        result = pool.map(process, [(url, payload) for url in urls])

    # DSPからのレスポンスを集計
    result = [x for x in result if x]

    if len(result) == 1:
        ad_url = result[0][0]
        price = 1
    elif len(result) == 0:
        ad_url = AD_URL + str(app_id)
        price = 0
    else:
        result.sort(key=lambda x: x[1], reverse=True)
        ad_url = result[0][0]
        price = result[1][1]

    # DSPにWinNoticeを送信
    win_url = result[0][2]
    win_payload = {"request_id": request_id, "price": price}
    win_response = requests.post(win_url+"/win", json.dumps(win_payload), headers=HEADERS).json()

    # SDKにレスポンスを送信
    response = {"url": ad_url}
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(threaded=True)
