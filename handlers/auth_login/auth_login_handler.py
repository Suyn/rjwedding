# coding=utf8
from handlers.base.base_handler import BaseHandler
from libs.verification_code.captcha import create_captcha_img, auth_captcha, auth_login, auth_mobile_code, auth_regist


class AuthloginHandler(BaseHandler):
    def get(self):
        self.render('auth_login.html')

    def post(self):
        username = self.get_argument('name', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')

        result = auth_captcha(self, code, captcha)
        print('数据提交成功')
        print(result['msg'])
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        result = auth_login(self, username, password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class CaptchaHandler(BaseHandler):
    def get(self, *args, **kwargs):
        code = self.get_argument('code', '')
        pre_code = self.get_argument('pre_code', '')
        img = create_captcha_img(self, code, pre_code)
        self.set_header("Content-Type", "image/jpg")
        self.write(img)

##########################################

class AuthregistHandler(BaseHandler):
    def get(self):
        self.render('auth_regist.html', message='欢迎注册')

    def post(self):
        mobile = self.get_argument('mobile' '')
        mobile_captcha = self.get_argument('mobile_captcha', '')
        name = self.get_argument('name', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        captcha = self.get_argument('captcha', '')
        code = self.get_argument('code', '')
        result = auth_regist(self, mobile, mobile_captcha, name, password1, password2, captcha, code)
        if result['status'] is True:
            return self.write({'status': '200', 'msg': result['msg']})
        return self.write({'status': '400', 'msg': result['msg']})


class AuthmobilecodeHandler(BaseHandler):
    def post(self):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        result = auth_mobile_code(self, mobile, code, captcha)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        return self.write({'status': 200, 'msg': result['msg']})

auth_login_handler = [(r'/auth/login', AuthloginHandler)]
captcha_handler = [(r'/auth/captcha', CaptchaHandler)]
auth_regist_handler = [(r'/auth/regist', AuthregistHandler)]
auth_mobilecode_handler = [(r'/auth/mobile_code', AuthmobilecodeHandler)]
