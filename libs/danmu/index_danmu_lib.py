# coding=utf8
from datetime import datetime
from models.danmu_module.danmu_table import Danmu
import json


def danmu_lists(self):
    # contents = []
    # with open('templates/danmu.txt') as f:
    #     for i in f.readlines():
    #         c = json.loads(i)
    #         contents.append(c['Content'])
    # return contents
    conts = []
    alls = Danmu.get_all()
    for i in alls:
        conts.append('%s: %s' % (i.username, i.contents))
    return conts


def danmu_lib(self, danmu):
    if self.get_current_user() is None:
        return {'status': False, 'msg': '需要先登录才能发表祝福哦~'}
    if danmu is None or len(danmu) == 0:
        return {'status': False, 'msg': '您的祝福内容为空'}
    if len(danmu) > 64:
        return {'status': False, 'msg': '祝福内容不可超过64个字'}
    if '\\' in danmu:
        danmu = danmu.replace('\\', '')
    if '<br>' in danmu:
            danmu = danmu.replace('<br>', '')
    d = Danmu()
    d.username = self.get_current_user()
    d.contents = danmu
    self.db.add(d)
    self.db.commit()
    # danmu = {"User": "".replace('', self.get_current_user()), "Time": "%s" % datetime.now(), "Content": "".replace('', danmu)}
    # print danmu
    # with open("templates/danmu.txt", "a+") as f:
    #     f.write(json.dumps(danmu) + '\n')
    return {'status': True, 'msg': '感谢您的祝福'}
