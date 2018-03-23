# coding=utf-8
from __future__ import absolute_import
from utils.send_email.send_email_libs import send_qq_html_email
import time
import redis, json
from celery_module.celery import celery_test
conn = redis.Redis()


# @celery_test.task
# def add(a, b):
#     time.sleep(2)
#     return a+b

@celery_test.task
def manage_redis():
    regist_email_list = conn.keys("*regist_email:*")
    print regist_email_list
    if regist_email_list:
        for i in regist_email_list:
            org_regist_data = conn.get(i)
            print org_regist_data
            regist_data = json.loads(org_regist_data)
            if regist_data['IsSendEmail'] == 'no':
                e_mail_list = []
                e_mail_list.append(regist_data['email'])
                email_code = regist_data['email_code']
                print email_code
                content = """
                您好，<a href="http://wulilove.cn">WuLilove</a>提醒您，您的验证码为<span style="color: blue">{}</span>,有效时间为30分钟，若非您本人所为请忽略此邮件。
                """.format(email_code)
                send_qq_html_email("wedding@wulilove.cn", e_mail_list, "注册", content)
                modify_regist_data = org_regist_data.replace('no', 'yes')
                conn.setex('regist_email:%s' % regist_data['email'], modify_regist_data, 1800)
