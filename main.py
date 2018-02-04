# coding=utf8
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from config import settings
from handlers.all.all_handlers import handlers
from libs.db.create_tables import run

# import util.ui_method
# import util.ui_module
# 定义一个默认的端口
define("port", default=9000, help="run port ", type=int)
# 创建表单
define("t", default=False, help="create a table", type=bool)


if __name__ == "__main__":
    print('正在启动服务器......')
    options.parse_command_line()
    if options.t:
        run()
    app = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('已启用默认{}端口'.format(options.port))
    print('服务器已启动！')
    tornado.ioloop.IOLoop.instance().start()
