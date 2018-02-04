# coding=utf8
from utils.captcha.captcha import create_captcha
from models.acount_user_modules.user_modules import session, User
from datetime import datetime
from random import randint
from utils.yun_tong_xun.yun_tong_xun import sendTemplateSMS


def create_captcha_img(self, code, pre_code):
    if pre_code:
        self.conn.delete("captcha:%s" % pre_code)
    text, img = create_captcha()
    self.conn.setex("captcha:%s" % code, text.lower(), 60)
    return img


def auth_captcha(self, code, captcha):
    if captcha == '':
        return {'status': False, 'msg': '请输入验证码'}
    elif self.conn.get("captcha:%s" % code) == captcha.lower():
        return {'status': True, 'msg': '正确'}
    return {'status': False, 'msg': '输入的验证码错误'}


def auth_login(self, username, password):
    if username == '':
        return {'status': False, 'msg': '请输入用户名'}
    if password == '':
        return {'status': False, 'msg': '请输入密码'}
    username = User.get_username(username)
    if username and username.auth_password(password):
        self.session.set('user', username.username)
        username.login_num += 1
        username.last_login = datetime.now()
        session.add(username)
        session.commit()
        return {'status': True, 'msg': '登录成功'}
    return{'status': False, 'msg': '用户名或密码错误'}


def auth_mobile_code(self, mobile, code, captcha):
    if isinstance(mobile, unicode):
        mobile = mobile.encode('utf-8')
    if captcha == '':
        return {'status': False, 'msg': '请输入验证码'}
    elif self.conn.get("captcha:%s" % code) != captcha.lower():
        return {'status': False, 'msg': '输入的验证码错误'}
    mobile_code = '{}{}{}{}{}{}'.format(randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9))
    self.conn.setex("mobile_code:%s" % mobile, mobile_code, 600)
    print '手机验证码为' + mobile_code
    #---
    sendTemplateSMS(mobile, [mobile_code, 10], 1)
    return {'status': 200, 'msg': '%s' % mobile}


def auth_regist(self, mobile, mobile_captcha, name, password1, password2, captcha, code):
    if captcha == '':
        return {'status': False, 'msg': '请输入验证码'}
    elif self.conn.get("captcha:%s" % code) != captcha.lower():
        return {'status': False, 'msg': '输入的验证码错误'}
    if name == '':
        return {'status': False, 'msg': '昵称为空'}
    if password1 != password2:
        return {'status': False, 'msg': '您两次输入的密码不一致'}
    if not self.conn.get("mobile_code:%s" % mobile):
        return {'status': False, 'msg': '请检查您的手机号是否已更改或刷新页面重试'}
    if self.conn.get("mobile_code:%s" % mobile) != mobile_captcha:
        return {'status': False, 'msg': '您输入的验证码不正确'}
    self.db.add(User(mobile=mobile, username=name, password=password1))
    self.db.commit()
    return {'status': True, 'msg': '注册成功'}
