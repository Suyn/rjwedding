# coding=utf8
from handlers.base.base_handler import BaseHandler
# from handlers.autherror.autherror_handler import AuthError
from models.acount_user_modules.user_modules import User
from random import randint
import json


class RegistHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('sign-up.html', error=None)

    def post(self, *args, **kwargs):
        result = self._checkit()
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        self.session.delete("user")
        return self.write({'status': 200, 'msg': result['msg']})

    def _checkit(self):
        el = self.get_argument('email')
        un = self.get_argument('yourname')
        pd1 = self.get_argument('password1')
        pd2 = self.get_argument('password2')
        username = User.get_username(un)
        email = User.get_email(el)
        if 2 <= len(un) < 25 and 5 < len(el) < 30 and 5 < len(pd1) == len(pd2) < 64:
            if not username and not email and pd1 == pd2:
                email_num_code = '{}{}{}{}{}{}'.format(randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9))
                print "邮箱验证码为%s" % email_num_code
                user_data = {'email': el,
                             'username': un,
                             'password': pd1,
                             'email_code': email_num_code,
                             'IsSendEmail': 'no'}
                if self.conn.get("regist_email:%s" % el):
                    self.conn.delete("regist_email:%s" % el)
                self.conn.setex("regist_email:%s" % el, json.dumps(user_data), 1800)
                return {'status': True, 'msg': '验证码已发送至您的邮箱，请注意查收'}
                # self._submit(un, el, pd1)
                # return {'status': True, 'msg': '注册成功'}
                #
            else:
                if username:
                    return {'status': False, 'msg': '该用户名已被注册'}
                    # raise AuthError('该用户名已被注册')
                elif email:
                    return {'status': False, 'msg': '该邮箱已被注册'}
                    # raise AuthError('该邮箱已被注册')
                else:
                    return {'status': False, 'msg': '您两次输入的密码不相等'}
                    # raise AuthError('您两次输入的密码不相等')
        else:
            return {'status': False, 'msg': '您的用户名或邮箱或密码格式不正确，请仔细检查'}
            # raise AuthError('您的用户名或邮箱或密码格式不正确，请仔细检查')


class EmailCodeHandler(BaseHandler):
    def get(self):
        email_num = self.get_argument('email_num', '')
        if email_num is None or email_num == '':
            return self.redirect('/404')
        return self.render('email_code.html', user_email=email_num)

    def post(self):
        email_code = self.get_argument('email_code', '')
        email_num = self.get_argument('email_num', '')
        if email_num is None or email_num == '':
            return self.write({'status': 400, 'msg': '请重新回到注册页填写注册信息'})
        if email_code == '':
            return self.write({'status': 400, 'msg': '您输入的邮箱验证码为空'})
        user_data = self.conn.get("regist_email:%s" % email_num)
        if user_data is not None:
            user_data = json.loads(user_data)
            if user_data['email'] == email_num and user_data['email_code'] == email_code:
                self._submit(user_data['username'], user_data['email'], user_data['password'])
                self.conn.delete("regist_email:%s" % email_num)
                return self.write({'status': 200, 'msg': '注册成功'})
            return self.write({'status': 400, 'msg': '验证码有误，请重新输入'})
        return self.write({'status': 400, 'msg': '验证失败，请重新回到注册页填写注册信息'})

    def _submit(self, un, email, pd):
        self.db.add(User(username=un, email=email, password=pd))
        self.db.commit()


regist_handler = [(r'/regist', RegistHandler),
                  (r'/email_code', EmailCodeHandler)]
