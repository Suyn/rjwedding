# -*- coding:utf-8 -*-
from handlers.base.base_handler import BaseHandler
from tornado.web import authenticated
from models.acount_user_modules.user_modules import User
from libs.modify_center_lib.modify_center_lib import modify_center_lib
from models.danmu_module.danmu_table import Danmu
from utils.send_email.send_email_libs import send_qq_html_email
import time
import json


# class ModifyCenterHandler(BaseHandler):
#     def get(self):
#         if not self.current_user:
#             return self.render('modify.html', current_user=None, default_avatar=None)
#         current_user = User.get_username(self.current_user)
#         return self.render('modify.html', current_user=current_user, default_avatar=current_user.avatar)


class ModifyAvatarHandler(BaseHandler):
    def post(self):
        avatar_data = self.request.files.get('user_avatar', '')
        if avatar_data is None or avatar_data == '':
            return
        result = modify_center_lib(self, avatar_data[0]['body'])
        if result['status'] is True:
            return self.redirect('/modify_center_1')
        return self.write(result['msg'])


class ModifyCenterOneHandler(BaseHandler):
    def get(self):
        user_exit_current = self.current_user
        if user_exit_current:
            current_user = User.get_username(user_exit_current)
            user_data = Danmu().get_all_personal(user_exit_current)
            user_data_list = []
            for i in user_data:
                c = {'name': current_user.username, 'useravatar': current_user.avatar,
                     'datetime': i.creattime, 'content_html': i.contents,
                     'content_user_id': i.id}
                user_data_list.append(c)
            user_data_list.reverse()
            return self.render('modify_center_1.html', current_user=current_user, cache=user_data_list)
        return self.write('您还未登录')


class ModifyEmailHandler(BaseHandler):
    def post(self):
        new_email = self.get_argument('modify_email', '')
        real_exit = User.get_email(new_email)
        if new_email == '':
            return self.redirect('/modify_center_1')
        if not real_exit:
            e_mail_list = []
            e_mail_list.append(new_email)
            date_time = round(time.time(), 1)
            current_email = User.get_username(self.current_user).email
            user_data = {'code_times': date_time, 'current_email': current_email, 'new_email': new_email}
            if self.conn.get("modify_email:%s" % current_email):
                self.conn.delete("modify_email:%s" % current_email)
            self.conn.setex("modify_email:%s" % current_email, json.dumps(user_data), 1800)
            content = """
            您好，<a href="http://wulilove.cn">WuLilove</a>提醒您，您正在执行修改邮箱操作，请点击此链接
            http://wulilove.cn/modify_confirm_email?current_email={}&new_email={}&code_times={}; 有效时间为30分钟，若非您本人所为请忽略此邮件。
            """.format(current_email, new_email, date_time)
            send_qq_html_email("wedding@wulilove.cn", e_mail_list, "修改邮箱", content)
            return self.redirect('/modify_center_1')
        return self.write('该邮箱已被注册！')


class ModifyConfirmEmailHandler(BaseHandler):
    def get(self):
        current_email = self.get_argument('current_email', '')
        new_email = self.get_argument('new_email', '')
        times = self.get_argument('code_times', '')
        print(len(times))
        print times
        if times and current_email and new_email:
            datas = json.loads(self.conn.get("modify_email:%s" % current_email))
            if datas and str(datas['code_times']) == times and datas['current_email'] == current_email and datas['new_email'] == new_email:
                user = User.get_email(current_email)
                user.email = new_email
                self.db.add(user)
                self.db.commit()
                return self.write('修改邮箱成功')
            return self.write('修改邮箱失败')
        return self.redirect('/404')


class ModifyDeleteContents(BaseHandler):
    def get(self):
        content_id = self.get_argument('current_content_id', '')
        if content_id == '':
            return self.redirect('/modify_center_1')
        content_id = Danmu.get_id(content_id)
        if content_id is not None and content_id.username == self.current_user:
            self.db.delete(content_id)
            self.db.commit()
            return self.redirect('/modify_center_1')
        return self.redirect('/modify_center_1')

modify_center_handler = [(r'/modify_avatar', ModifyAvatarHandler),
                         (r'/modify_center_1', ModifyCenterOneHandler),
                         (r'/modify_email', ModifyEmailHandler),
                         (r'/modify_confirm_email', ModifyConfirmEmailHandler),
                         (r'/modify_content_delete', ModifyDeleteContents)]

