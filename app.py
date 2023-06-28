import time
import xmltodict
from flask import Flask, request, abort
import hashlib
import localMysqlConnector

app = Flask(__name__)


# 回复信息标准化 类型为text
def replyMsg(toUserName, userID, content):
    return {
        'xml': {
            'ToUserName': toUserName,
            'FromUserName': userID,
            'CreateTime': int(time.time()),
            'MsgType': "text",
            'Content': content
        }
    }


# 检测请求是否合法
def checkAuth(timestamp, nonce):
    token = localMysqlConnector.getConfig()[0]
    list1 = [token, timestamp, nonce]
    # 排序
    list1.sort()
    # 把列表转换成字符串
    str1 = "".join(list1)
    # 生成sha1值
    return hashlib.sha1(str1.encode("utf-8")).hexdigest()


@app.route('/', methods=["GET", "POST"])
def wechat():
    # 微信服务器发来的三个get参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    # 与signature参数比对
    # 若不一致
    if signature != checkAuth(timestamp, nonce):
        # 被认定为非微信服务器发来的get请求
        # 返回403拒接请求
        abort(403)
    # 若一致
    else:
        if request.method == "POST":
            # 将xml数据包转换为字典
            msg = xmltodict.parse(request.data).get('xml')
            msgType = msg.get('Content')
            toUserName = msg.get('ToUserName')
            userID = msg.get('FromUserName')
            Content = "测试成功"
            # 数据打包成xml格式
            result = xmltodict.unparse(replyMsg(userID, toUserName, Content))
            return result


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='127.0.0.1')
