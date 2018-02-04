from handlers.index.index_handler import index_handler
from handlers.login.login_handler import login_handler
from handlers.regist.regist_handler import regist_handler
from handlers.forget.forget_handler import forget_handler, send_email_handler, found_password_handler
from handlers.auth_login.auth_login_handler import (auth_login_handler, captcha_handler,
                                                    auth_regist_handler, auth_mobilecode_handler,
                                                    )
from handlers.danmu.danmu_handler import danmu_handler
from handlers.error404.error404 import error_404_handler, error_other_handler
from handlers.message_websocket.send_message_handler import message_handler
from handlers.modify_center.modify_center import modify_center_handler


handlers = [

]
handlers += index_handler
handlers += login_handler
handlers += regist_handler
handlers += forget_handler
handlers += send_email_handler
handlers += found_password_handler

handlers += message_handler
handlers += modify_center_handler

handlers += auth_login_handler
handlers += captcha_handler
handlers += auth_regist_handler
handlers += auth_mobilecode_handler
handlers += danmu_handler




handlers += error_404_handler
handlers += error_other_handler
