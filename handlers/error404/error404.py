# -*- coding:utf-8 -*-
from handlers.base.base_handler import BaseHandler


class Error_404_Handler(BaseHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        else:
            self.write('error:' + str(status_code))


class Error404(BaseHandler):
    def get(self):
        return self.render('404.html')
error_404_handler = [(r'/404', Error404),
                     (r'.*', Error_404_Handler)]
error_other_handler = [(r'.*\..*', Error_404_Handler)]
