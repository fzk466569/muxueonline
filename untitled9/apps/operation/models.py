# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
	name = models.CharField(max_length=20, verbose_name=u"姓名")
	mobile = models.CharField(max_length=11, verbose_name=u"手机号")
	course_name = models.CharField(max_length=50, verbose_name=u"课程名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户咨询"
		verbose_name_plural = verbose_name


class CourseComments(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u"用户名称")
	course = models.ForeignKey(Course, verbose_name=u"课程名称")
	comments = models.CharField(max_length=200, verbose_name=u"评论")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户评论"
		verbose_name_plural = verbose_name


class UserFavorite(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u"用户名称")
	fav_id = models.IntegerField(default=0, verbose_name=u"数据ID")
	fav_type = models.CharField(choices=((1, '课程'), (2, '讲师'), (3, '机构')), default=1, max_length=10, verbose_name=u"收藏类型")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"收藏时间")

	class Meta:
		verbose_name = u"用户收藏"
		verbose_name_plural = verbose_name


class UserMessage(models.Model):
	user_id = models.IntegerField(default=0, verbose_name=u"接收用户")
	message = models.CharField(max_length=500, verbose_name=u"消息内容")
	is_read = models.BooleanField(default=False, verbose_name=u"是否已读")
	send_time = models.DateTimeField(default=datetime.now, verbose_name=u"接收时间")

	class Meta:
		verbose_name = u"用户消息"
		verbose_name_plural = verbose_name


class UserCourse(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u"接收用户")
	course = models.ForeignKey(Course, verbose_name=u"课程名称")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


	class Meta:
		verbose_name = u"用户课程"
		verbose_name_plural = verbose_name
