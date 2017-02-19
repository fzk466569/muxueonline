# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.


class CityDict(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"城市名称")
	desc = models.TextField(verbose_name=u"城市描述")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"城市"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class CourseOrg(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"机构名称")
	brief = models.CharField(max_length=15, verbose_name=u'机构简介', null=True, blank=True)
	desc = models.TextField(verbose_name=u"机构描述")
	students = models.IntegerField(default=0, verbose_name=u'学生人数')
	course_num = models.IntegerField(default=0, verbose_name=u'课程数')
	category = models.CharField(max_length=20, choices=(('pxjg', u'培训机构'), ('gr', u'个人'), ('gx', u'高校')),
	                            default='pxjg', verbose_name=u'机构类别')
	tag = models.CharField(default=u'全国著名', verbose_name=u'机构标签', max_length=20)
	click_nums = models.IntegerField(default=0, verbose_name=u"点击次数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏次数")
	image = models.ImageField(upload_to="org/%Y/%m", max_length=100, verbose_name="logo")
	address = models.CharField(max_length=100, verbose_name=u"机构地址")
	city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"课程机构"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_teacher_num(self):
		return self.teacher_set.all().count()


class Teacher(models.Model):
	org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
	name = models.CharField(max_length=50, verbose_name=u"教师姓名")
	age = models.IntegerField(default=0, verbose_name=u"年龄", null=True, blank=True)
	image = models.ImageField(upload_to="teacher/%Y/%m", default='', verbose_name=u"教师头像", max_length=100)
	work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
	work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
	work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
	points = models.CharField(max_length=50, verbose_name=u"教学特点")
	click_nums = models.IntegerField(default=0, verbose_name=u"点击次数")
	fav_nims = models.IntegerField(default=0, verbose_name=u"收藏次数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"教师"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_course_num(self):
		return self.course_set.all().count()
