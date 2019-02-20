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
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config.update({"DEBUG": True})

DSP_COUNT = 8
HEADERS = {"content-type": "application/json"}

def process(args):
    try:
        return send_request(*args)
    except TimeoutError:
        return None

@timeout(0.1)
def send_request(request_url, payload):
    response = requests.post(request_url, json.dumps(payload), headers=HEADERS).json()
    response_url = response.get("url")
    price = response.get("price")
    return (response_url, price)

@app.route("/req", methods=["POST"])
def req():
    # SDKからリクエストを受信
    now = datetime.now()
    request_time = now.strftime("%Y%m%d-%H%M%S.") + str(now.microsecond)[:4]
    app_id = request.json.get("app_id")
    ssp_name = "y_sako"
    request_id = ssp_name + "-" + str(uuid.uuid4())

    # DSPにリクエストを送信
    request_urls = ["http://" + config["host"][key] + "/req" for key in config["host"]]
    payload = {
        "ssp_name": ssp_name,
        "request_time": request_time,
        "request_id": request_id,
        "app_id": app_id
    }

    n_cores = multi.cpu_count()
    with Pool(n_cores) as pool:
        result = pool.map(process, [[request_url, payload] for request_url in request_urls])

    # DSPからのレスポンスを集計
    result = [x for x in result if x]

    if len(result) == 1:
        response_url = result[0][0]
        price = 1
    elif len(result) == 0:
        response_url = "http://example.com/ad/image/" + str(app_id)
        price = 0
    else:
        result.sort(key=lambda x: x[1], reverse=True)
        response_url = result[0][0]
        price = result[1][1]

    # DSPにWinNoticeを送信
    win_url = "http://localhost:6000/win"
    win_payload = {"request_id": request_id, "price": price}
    win_response = requests.post(win_url, json.dumps(win_payload), headers=HEADERS).json()
    if not win_response.get("result") == "ok":
        return make_response(jsonify(win_payload))

    # SDKにレスポンスを送信
    response = {"url": response_url}
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(threaded=True)
