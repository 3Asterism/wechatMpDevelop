#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import hashlib

# 微信的token令牌 此类用于过微信开发者验证
WECHAT_TOKEN = "111"

app = Flask(__name__)


@app.route('/test', methods=["GET"])
def wechat2():
    return 'helloWorld'


@app.route('/', methods=["GET"])
def wechat():
    """对接微信公众号服务器"""
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    # 校验参数
    if not all([signature, timestamp, nonce]):
        abort(400)

    # 按照微信的流程进行计算签名
    array = [WECHAT_TOKEN, timestamp, nonce]
    # 排序
    array.sort()
    # 拼接字符串
    tmp_str = "".join(array)
    # 进行sha1加密，得到正确的签名值
    sign = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
    print(sign == signature)
    # 将自己计算的签名值与请求的签名参数进行对比
    if signature != sign:
        abort(403)
    else:
        return echostr


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='127.0.0.1')
