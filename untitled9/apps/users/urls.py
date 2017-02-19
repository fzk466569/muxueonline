# _*_ coding: utf-8 _*_
from django.conf.urls import url

from .views import UserInfoView, ImageUploadView, ChangePWDView, SendMailCodeView, UpdateEmailView, MyCourseView, \
	MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

__author__ = 'fzk'
__date__ = '2017/2/10 0010 10:56'

urlpatterns = [
	url(r'^center/', UserInfoView.as_view(), name='user_info'),
	url(r'^image/', ImageUploadView.as_view(), name='image_upload'),
	url(r'^change/pwd/', ChangePWDView.as_view(), name='pwd_change'),
	url(r'^sendmail_code/', SendMailCodeView.as_view(), name='sendmail_code'),
	url(r'^update_email/', UpdateEmailView.as_view(), name='update_email'),
	url(r'^my_course/', MyCourseView.as_view(), name='my_course'),
	url(r'^my_fav/org/', MyFavOrgView.as_view(), name='my_fav_org'),
	url(r'^my_fav/teacher/', MyFavTeacherView.as_view(), name='my_fav_teacher'),
	url(r'^my_fav/course/', MyFavCourseView.as_view(), name='my_fav_course'),
	url(r'^my_message/', MyMessageView.as_view(), name='my_message'),

]
