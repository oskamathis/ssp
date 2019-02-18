# coding: utf-8

from flask import Flask, request, jsonify, make_response
app = Flask(__name__)
app.config.update({'DEBUG': True })


@app.route("/req", methods=['POST'])
def req():
    # SDKからリクエストを受信
    params = request.json
    app_id = params.get('app_id')

    # DSPにリクエストを送信

    # DSPからレスポンスを受信・集計

    # SDKにレスポンスを送信
    response = {}
    response.setdefault('url', 'http://example.com/ad/image/' + str(app_id))
    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run()
