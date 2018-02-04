# coding=utf8


class AuthError(Exception):
    def __init__(self, mg):
        super(AuthError, self).__init__(mg)
