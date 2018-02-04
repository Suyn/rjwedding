# coding=utf8
import tornado.web
import tornado.websocket
from pycket.session import SessionMixin
from libs.db.connect import session
from libs.redis_conn.redis_conn import conn


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db = session
        self.conn = conn
        self.flashes = None

    def get_current_user(self):
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None

    def on_finish(self):
        self.db.close()


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    def initialize(self):
        self.db = session
        self.conn = conn
        self.flashes = None

    def get_current_user(self):
        current_user = self.session.get("user")
        if current_user:
            return current_user
        return None

    def on_finish(self):
        self.db.close()
