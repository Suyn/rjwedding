# coding=utf8
from handlers.base.base_handler import BaseHandler
from libs.danmu.index_danmu_lib import danmu_lib


class DanmuHandler(BaseHandler):
    def post(self):
        danmu = self.get_argument('cong', None)
        result = danmu_lib(self, danmu)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

danmu_handler = [(r'/congratulation', DanmuHandler)]
