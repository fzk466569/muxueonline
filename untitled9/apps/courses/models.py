# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from DjangoUeditor.models import UEditorField

from django.db import models
from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
	course_org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构', null=True, blank=True)
	name = models.CharField(max_length=50, verbose_name=u"课程名称")
	desc = models.CharField(max_length=300, verbose_name=u"课程描述")
	is_banner = models.BooleanField(default=False, verbose_name=u'广告位')
	detail = UEditorField(default='', verbose_name=u'课程详情', width=600, height=300, imagePath="course/ueditor/",
	                      filePath="course/ueditor/")
	teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
	category = models.CharField(verbose_name=u'课程类别', max_length=20, default='后端开发')
	degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=5, verbose_name=u"课程难度")
	learn_times = models.IntegerField(default=0, verbose_name=u"学习时间")
	student = models.IntegerField(default=0, verbose_name=u"学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	youneed_knew = models.CharField(default='', max_length=200, verbose_name=u'课程须知')
	learn_about = models.CharField(default='', max_length=200, verbose_name=u'通过本课程后能学到的')
	tag = models.CharField(default='', max_length=50, verbose_name=u'课程标签')
	image = models.ImageField(upload_to="course/%Y/%m", verbose_name=u"课程首页图片", max_length=100)
	click_nums = models.IntegerField(default=0, verbose_name=u"点击次数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")

	class Meta:
		verbose_name = u"课程"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_zj_nums(self):
		return self.lesson_set.all().count()

	get_zj_nums.short_description = u"章节数"

	def get_user_course(self):
		return self.usercourse_set.all()

	def get_lessons(self):
		return self.lesson_set.all()

	def get_course_resources(self):
		return self.courseresource_set.all()


class BannerCourse(Course):
	class Meta:
		verbose_name = u'轮播图'
		verbose_name_plural = verbose_name
		proxy = True


class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程名称")
	name = models.CharField(max_length=100, verbose_name=u"章节名称", default=u'第一章：')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")

	class Meta:
		verbose_name = u"章节"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_videos(self):
		return self.video_set.all()


class Video(models.Model):
	lesson = models.ForeignKey(Lesson, verbose_name=u"课程名称")
	name = models.CharField(max_length=100, verbose_name=u"视频名称", default=u'第一节：')
	url = models.CharField(max_length=100, default='', verbose_name=u"视频链接")
	learn_times = models.IntegerField(default=0, verbose_name=u"视频时长")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")

	class Meta:
		verbose_name = u"视频"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程名称")
	name = models.CharField(max_length=100, verbose_name=u"课件名称")
	download = models.FileField(upload_to="course/resource/%Y%m", verbose_name=u"资源文件", max_length=100)
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")

	class Meta:
		verbose_name = u"资源文件"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name
