# -*- coding:utf-8 -*-
from handlers.base.base_handler import BaseHandler, BaseWebSocketHandler
from models.acount_user_modules.user_modules import User
import tornado.escape
from datetime import datetime
from models.danmu_module.danmu_table import Danmu
import time

class MessageIndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            current_user = User.get_username(self.current_user)
            user_data = Danmu().get_all()
            user_data_list = []
            for i in user_data:
                person = User.get_username(i.username)
                c = {'name': person.username, 'useravatar': person.avatar,
                     'datetime': i.creattime, 'content_html': i.contents}
                user_data_list.append(c)
            user_data_list.reverse()
            return self.render('message_websocket.html', current_user=current_user, cache=user_data_list)
        return self.write('您还未登录')


class SendBlessingHandler(BaseWebSocketHandler):
    users = {}# {'zhangsan': MessageWebSocket(), 'lishi': MessageWebSocket()}

    @classmethod
    def send_system_message(cls,self ,content,send_type):
        target = 'system'
        redis_msg = cls.dict_to_json(self, content, send_type, target)
        self.conn.rpush('message:%s'%send_type,redis_msg)
        for f, v in SendBlessingHandler.users.iteritems():
            v.write_message(redis_msg)

    @classmethod
    def dict_to_json(cls, self, content, send_type, target):
        msg = {
            "content": content,
            "send_type": send_type,
            "sender": self.current_user.name,
            "target": target,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return tornado.escape.json_encode(msg)

    @classmethod
    def send_user_message(cls, self,content,send_type,user):
        redis_msg = cls.dict_to_json(self, content, send_type, user)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        if cls.users.get(user, None) is not None:
            cls.users[user].write_message(redis_msg)
        else:
            #self.conn.lpush("ws:user_off_line",message)
            pass

    def open(self):
        print '----------------open------------------'
        SendBlessingHandler.users[User.get_username(self.current_user).username] = self
        # self.conn.rpush('message:user_list', User.get_username(self.current_user))
        # # users['zhangsan'] = self
        # # users['lishi'] =self
        # print SendBlessingHandler.users
        # SendBlessingHandler.send_system_message(
        #     self, "%s:上线了" % self.current_user.name.encode('utf-8'), "system", )

    def on_close(self):
        print '---------------close------------------'
        del SendBlessingHandler.users[User.get_username(self.current_user).username]

    def on_message(self, message):
        print '---------------on_message------------------'
        print message
        msg = tornado.escape.json_decode(message)
        if msg['content_html'] == '' or len(msg['content_html']) > 65:
            return
        if '\n' in msg['content_html']:
            msg['content_html'] = msg['content_html'].replace('\n', '')
        if '<br>' in msg['content_html']:
            msg['content_html'] = msg['content_html'].replace('<br>', '')
        if '\\' in msg['content_html']:
            msg['content_html'] = msg['content_html'].replace('\\', '')
        if msg['content_html'] != '' and len(msg['content_html']) < 65:
            msg.update({
                "name": User.get_username(self.current_user).username,
                "useravatar": User.get_username(self.current_user).avatar,
                "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+46800))
            })
            blessing = Danmu(username=self.current_user, contents=msg['content_html'])
            self.db.add(blessing)
            self.db.commit()
            # message = tornado.escape.json_encode(msg)
            #
            # self.conn.rpush('message:list', message)
            #
            for f, v in SendBlessingHandler.users.iteritems():
                v.write_message(msg)

message_handler = [(r'/blessing_circle', MessageIndexHandler),
                   (r'/send_blessing', SendBlessingHandler)]
