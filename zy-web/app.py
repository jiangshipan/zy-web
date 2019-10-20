# coding=utf-8
import json
from flask import Flask, request, make_response
from geventwebsocket.websocket import WebSocket, WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from common.util.zy_util import unicode_to_dict, upload_file, check_token, check_ws_token
from service.user_service import UserService

app = Flask(__name__)
# 最大上传文件大小
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# 当前在线人数
user_socket_dict = {}


@app.route('/getOnline')
def show_online_user():
    return {"data": user_socket_dict.keys()}


@app.route('/send_to_all/<send_msg>')
@check_token
def send_to_all(send_msg):
    for _, u_socket in user_socket_dict.items():
        u_socket.send(send_msg)
    return {"data": "success"}


@app.route('/ws/<login_token>')
def ws(login_token):
    username, flag = check_ws_token(login_token)
    if not flag:
        print login_token, "permit denied"
        return {"data:": "permit denied"}
    user_socket = request.environ.get("wsgi.websocket")
    print username, "success come in"
    if not user_socket:
        return {"data": "please use websocket"}
    user_socket_dict[username] = user_socket
    while True:
        try:
            user_msg = user_socket.receive()
            user_msg = unicode_to_dict(user_msg)
            if not user_msg:
                continue
            print "%s发来的" % username, user_msg
            user_msg = dict(user_msg)
            send_msg = {
                'send_user': username,
                'send_msg': user_msg.get('message'),
                'target': user_msg.get('target')
            }
            send_to_one(send_msg)
        except WebSocketError as e:
            print e
            break
    user_socket.close()
    user_socket_dict.pop(username)
    return "over"


@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if not username or not password:
        return {"data": "username or password not is empty"}
    msg, flag = UserService().login(username, password)
    if not flag:
        return {"data": msg}
    resp = make_response('set_cookie')
    resp.set_cookie('login_token', msg)
    return resp


@app.route('/upload', methods=['POST'])
@check_token
def upload_img():
    if 'file' not in request.files:
        return {"data": "can't get file"}
    file = request.files['file']
    if file.filename == '':
        return "no selected file"
    msg = upload_file(file)
    return {"data": msg}


def send_to_one(send_msg):
    if not send_msg:
        return
    for username, u_socket in user_socket_dict.items():
        if username == send_msg.get('target'):
            u_socket.send(json.dumps(send_msg))
            print "已经发送给", send_msg.get('target')
            break


@app.after_request
def cors(environ):
    """
    解决跨域
    :param environ:
    :return:
    """
    environ.headers['Access-Control-Allow-Origin'] = 'http://localhost:3333'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    environ.headers['Access-Control-Allow-Credentials'] = 'true'
    return environ


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    pass
