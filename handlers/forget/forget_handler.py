# coding=utf8
import tornado.web
import time
from handlers.base.base_handler import BaseHandler
from models.acount_user_modules.user_modules import User, session
from utils.send_email.send_email_libs import send_qq_html_email


class ForgetHandler(BaseHandler):
    def get(self):
        self.render('forgot.html')

    def post(self):
        code = round(time.time(), 2)
        user = User.get_email(self.get_argument('email'))
        if user:
            e_mail_list = []
            e_mail_list.append(user.email)
            if self.conn.get("found_password:%s" % user.email):
                self.conn.delete("found_password:%s" % user.email)
            self.conn.setex("found_password:%s" % user.email, code, 1800)
            content = """
            您好，<a href='http://wulilove.cn'>wulilove.cn</a>网站提醒您，您正在进行找回密码操作,修改密码请点击此链接
            http://wulilove.cn/forget/send_email?e_mail={}&code={}，
            链接有效时间为30分钟，若非您本人所为请忽略此邮件。
            """.format(user.email, code)
            send_qq_html_email("wedding@wulilove.cn", e_mail_list, "找回密码", content)
            return self.write({'status': 200, 'msg': '发送成功，请到您的邮箱继续操作'})
        return self.write({'status': 400, 'msg': '该邮箱号码不存在'})


class SendEmailHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code', '')
        e_mail = self.get_argument('e_mail', '')
        print e_mail
        if e_mail is None:
            return self.render('404.html')
        if code is None:
            return self.render('404.html')
        if self.conn.get("found_password:%s" % e_mail) == code:
            return self.render('found_password.html', code=code, e_mail=e_mail)
        return self.render('404.html')


class FoundpasswordHandler(BaseHandler):
    def post(self):
        code = self.get_argument('code', '')
        e_mail = self.get_argument('e_mail', '')
        pd1 = self.get_argument('password1', '')
        pd2 = self.get_argument('password2', '')
        if pd1 == '' or pd2 == '':
            return self.write({'status': 400, 'msg': '请输入密码'})
        if pd1 != pd2:
            return self.write({'status': 400, 'msg': '两次输入的密码不一致'})
        if self.conn.get("found_password:%s" % e_mail) != code:
            return self.write({'status': 400, 'msg': '您可能在进行非法测试，我们将会对您的ip地址进行监测'})
        user = User.get_email(e_mail)
        user.password = pd1
        self.db.add(user)
        self.db.commit()
        self.conn.delete("found_password:%s" % e_mail)
        return self.write({'status': 200, 'msg': '修改密码成功'})


forget_handler = [(r'/forget', ForgetHandler)]
send_email_handler = [(r'/forget/send_email', SendEmailHandler)]
found_password_handler = [(r'/forget/found_password', FoundpasswordHandler)]
