# -*- coding:utf-8 -*-
from models.acount_user_modules.user_modules import User


def modify_center_lib(self, avartar_data):
    user = User.get_username(self.current_user)
    try:
        user.avatar = avartar_data
        self.db.add(user)
        self.db.commit()
        return {'status': True, 'msg': '头像修改成功'}
    except Exception as e:
        return {'status': False, 'msg': e}
