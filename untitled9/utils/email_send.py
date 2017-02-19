# _*_ coding: utf-8 _*_

from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from untitled9.settings import EMAIL_FROM

__author__ = 'fzk'
__date__ = '2017/2/5 0005 22:33'


def generate_random_str(randomlength=8):
	str = ''
	chars = 'ABCDEFGHIJKLMNOPQRSTUVYXYZabcdefghijklmnopqrstuvwxyz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def send_register_email(email, send_type='register'):
	email_record = EmailVerifyRecord()
	if send_type == 'reset_email':
		code = generate_random_str(6)
	else:
		code = generate_random_str(16)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()
	if send_type == 'register':
		email_title = u'慕学网注册激活链接'
		email_body = u'请点击下面链接激活您的账号：http://127.0.0.1:8000/active/{0}'.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass
	elif send_type == 'forget':
		email_title = u'慕学网密码重置链接'
		email_body = u'请点击下面链接重置您的密码：http://127.0.0.1:8000/reset/{0}'.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass
	elif send_type == 'reset_email':
		email_title = u'慕学网邮箱重置链接'
		email_body = u'您的邮箱验证码为：{0}'.format(code)
		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass
