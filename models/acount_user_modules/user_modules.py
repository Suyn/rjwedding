from datetime import datetime
from string import printable
from pbkdf2 import PBKDF2
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import time
from libs.db.connect import Base, session


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False)

    _password = Column('password', String(64))

    email = Column(String(40))
    password = Column(String(100))
    creattime = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+46800)))
    last_login = Column(DateTime, default=None)
    login_num = Column(Integer, default=0)
    mobile = Column(String(50))
    _avatar = Column(String(64))
    _locked = Column(Boolean, default=False, nullable=False)

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self._hash_password(value)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)
        return False

    @property
    def avatar(self):
        return self._avatar if self._avatar else "default_avatar.jpg"

    @avatar.setter
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/user_avatar/" + self._avatar):
                    os.unlink("static/images/user_avatar/" + self._avatar)
                file_path = str("static/images/user_avatar/" + str(self.id) + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = str(self.id) + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def get_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_email(cls, email):
        return session.query(cls).filter_by(email=email).first()

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def __repr__(self):
        return "<User(id='%s',username='%s',password='%s',creatime='%s',_locked='%s')>"%(
            self.id,
            self.username,
            self.password,
            self.creattime,
            self._locked
        )

# class Retuser(Base):
#     __tablename__ = 'retuser'
#     r_id = Column(Integer, primary_key=True, autoincrement=True)
#     last_login = Column(DateTime, default=datetime.now)
#     login_num = Column(Integer, default=0)
#     u_id = Column(Integer, ForeignKey('user.id'))

