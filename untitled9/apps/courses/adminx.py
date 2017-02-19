# _*_ coding: utf-8 _*_

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse

__author__ = 'fzk'
__date__ = '2017/2/4 0004 22:26'


class LessonInline(object):
	model = Lesson
	extra = 0


class VideoInline(object):
	model = Video
	extra = 0


class CourseResourceInline(object):
	model = CourseResource
	extra = 0


class CourseAdmin(object):
	list_display = ['name', 'desc', 'get_zj_nums', 'detail', 'is_banner', 'degree', 'learn_times', 'student', 'fav_nums',
	                'click_nums', 'add_time']
	search_fields = ['name', 'desc', 'detail', 'is_banner', 'degree', 'student', 'fav_nums', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'student', 'fav_nums', 'click_nums',
	               'add_time']
	ordering = ['-click_nums']
	readonly_fields = ['click_nums', 'fav_nums', 'student']
	exclude = ['click_nums']
	list_editable = ['desc', 'degree', 'is_banner']
	inlines = [LessonInline, CourseResourceInline]
	style_fields = {"detail": "ueditor"}

	def queryset(self):
		qs = super(CourseAdmin, self).queryset()
		qs = qs.filter(is_banner=False)
		return qs

	def save_models(self):
		obj = self.new_obj
		obj.save()
		if obj.course_org is not None:
			course_org = obj.course_org
			course_org.course_num = Course.objects.filter(course_org=course_org).count()
			course_org.save()


class BannerCourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'student', 'fav_nums', 'click_nums',
	                'add_time']
	search_fields = ['name', 'desc', 'detail', 'is_banner', 'degree', 'student', 'fav_nums', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'student', 'fav_nums', 'click_nums',
	               'add_time']
	ordering = ['-click_nums']
	readpnly_fields = ['click_nums', 'fav_nums']
	list_editable = ['desc', 'degree', 'is_banner']
	exclude = ['click_nums']
	inlines = [LessonInline, CourseResourceInline]

	def queryset(self):
		qs = super(BannerCourseAdmin, self).queryset()
		qs = qs.filter(is_banner=True)
		return qs


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name']
	list_filter = ['course__name', 'name', 'add_time']
	refiled_style = 'fk-ajax'

	inlines = [VideoInline]



class VideoAdmin(object):
	list_display = ['lesson', 'name', 'add_time']
	search_fields = ['lesson', 'name']
	list_filter = ['lesson__name', 'name', 'add_time']
	refiled_style = 'fk-ajax'


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['course', 'name', 'download']
	list_filter = ['course__name', 'name', 'download', 'add_time']
	refiled_style = 'fk-ajax'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
