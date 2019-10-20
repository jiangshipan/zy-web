# coding=utf-8

class UserService(object):
    def __init__(self):
        self.__user = {
            'jiangshipan': '123456',
            'zhangzhiyu': '123456',
            'yangboxin': '123456'
        }
        self.login_token = {
            'jiangshipan': '123456_login',
            'zhangzhiyu': 'qqqqq_login',
            'yangboxin': '123qqqe456'
        }

    def login(self, username, password):
        user_pass = self.__user.get(username)
        if not user_pass:
            return "user is not exist", False
        if user_pass != password:
            return "username or password is error", False
        return self.login_token[username], True
