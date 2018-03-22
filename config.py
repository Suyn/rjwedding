# coding:utf8
from libs.flash.flash_lib import get_flashed_messages
from libs.danmu.index_danmu_lib import danmu_lists

settings = dict(
    login_url='/auth/login',
    cookie_secret='abcdefghijklmnopqrstuvwxyz',
    # debug=True,
    template_path='templates',
    static_path='static',
    xsrf_cookies=True,
    ui_methods={'get_flashed_messages': get_flashed_messages,
                'danmu_lists': danmu_lists
                },
    # ui_modules=util.ui_module,
    pycket={
            'engine': 'redis',
            'storage': {
                'host': 'localhost',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2**31,
            },
            'cookies': {
                'expires_days': 1,
                'max_age': 3600
            }
        }
)
