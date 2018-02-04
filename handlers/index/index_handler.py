# coding=utf8
from handlers.base.base_handler import BaseHandler
from tornado.web import authenticated
import json,time
from models.acount_user_modules.user_modules import User
from models.danmu_module.danmu_table import Danmu


class IndexHandler(BaseHandler):
    # @authenticated
    def get(self):
        # contents = []
        # with open('templates/danmu.txt') as f:
        #     for i in f.readlines():
        #         c = json.loads(i)
        #         contents.append(c['Content'])
        # print(contents)
        date_regist = 0
        date_data = time.strftime('%Y-%m-%d', time.localtime(time.time()+46800))
        user_list = User.get_all()
        for create_time in user_list:
            c = create_time.creattime.strftime('%Y-%m-%d')
            if c == date_data:
                date_regist += 1
        print date_regist
        # --------------
        three_list = []
        three_contents = Danmu.get_all()[-3:]
        for i in three_contents:
            avatar = User.get_username(i.username).avatar
            name = i.username
            user_content = i.contents
            three_list.append((avatar, name, user_content))
        three_list.reverse()
        kw = {
            'username': self.current_user,
            'people': len(User.get_all()),
            'congratulations': len(Danmu.get_all()),
            'date_regist': date_regist,
            'user': three_list
        }
        self.render('index.html', **kw)

index_handler = [(r'/', IndexHandler)]
