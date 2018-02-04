# coding:utf8
from handlers.base.base_handler import BaseHandler
from models.acount_user_modules.user_modules import User, session
from handlers.autherror.autherror_handler import AuthError
from datetime import datetime
from libs.flash.flash_lib import flash
import time


class LoginHandler(BaseHandler):
    def get(self):
        nextname = self.get_argument('next', '/')
        if self.session.get('user'):
            self.redirect('/')
        else:
            self.render('sign-in.html', nextname=nextname, error=None)

    def post(self):
        try:
            nextname = self.get_argument('next', '/')
            username = User.get_username(self.get_argument('name', ''))
            email = User.get_email(self.get_argument('name', ''))
            password = self.get_argument('password')
            if not username and not email:
                raise AuthError('用户不存在')
            if username and username.auth_password(password):
                self.success_login(username)
                self.session.set('user', username.username)
                self.redirect(nextname)
            elif email and email.auth_password(password):
                self.success_login(email)
                self.session.set('user', email.username)
                self.redirect(nextname)
            else:
                raise AuthError('用户名或密码错误')
        except Exception as e:
            return self.render('sign-in.html', error=e, nextname=nextname)

    def success_login(self, user):
        user.login_num += 1
        user.last_login = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+46800))
        session.add(user)
        session.commit()

    # def post(self, *args, **kwargs):
    #     # nextname = self.get_argument('next', '')
    #     username = User.get_username(self.get_argument('name'))
    #     email = User.get_email(self.get_argument('name'))
    #     password = self.get_argument('password')
    #     if username and username.auth_password(password):
    #         self.success_login(username)
    #         self.session.set('user', username.username)
    #         # self.redirect(nextname)
    #     elif email and email.auth_password(password):
    #         self.success_login(email)
    #         self.session.set('user', email.username)
    #         # self.redirect(nextname)
    #     else:
    #         flash(self, "用户名或密码错误", "error")
    #         print '执行了flash'
    #         self.redirect('/login')

login_handler = [(r'/login', LoginHandler)]
