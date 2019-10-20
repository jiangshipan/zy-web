# coding=utf-8
import json
import os
import functools
from service.user_service import UserService

ALLOW_FILE_EXT = ['png', 'jpg', 'jpeg']
# UPLOAD_PATH = '/Users/jiangshipan/Downloads'
# UPLOAD_PATH = '/home/jiangshipan/jsp_repos/download'
UPLOAD_PATH = '/usr/xiaowan/www/jsp_download'


def unicode_to_dict(msg):
    try:
        msg = msg.encode('utf-8')
        return json.loads(msg)
    except Exception:
        return ""


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOW_FILE_EXT


def upload_file(file):
    if file and allow_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_PATH, filename))
        return 'http://www.wvue.com.cn/jsp_download/%s' % filename
    return 'only support png,jpg,jpeg file'


def check_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request
        login_token = request.cookies.get('login_token')
        login_tokens = UserService().login_token
        is_pass = False
        for k, v in login_tokens.items():
            if login_token == v:
                is_pass = True
                break
        if not is_pass:
            return {"data": "permit denied"}
        return func(*args, **kwargs)

    return wrapper


def check_ws_token(token):
    login_tokens = UserService().login_token
    for k, v in login_tokens.items():
        if v == token:
            return k, True
    return '', False
