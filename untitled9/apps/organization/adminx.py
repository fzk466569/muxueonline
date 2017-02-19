# _*_ coding: utf-8 _*_
__author__ = 'fzk'
__date__ = '2017/2/4 0004 22:50'
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
	list_display = ['name', 'desc', 'add_time']
	search_fields = ['name', 'desc']
	list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
	list_display = ['name', 'desc', 'category', 'click_nums', 'address', 'city', 'add_time']
	search_fields = ['name', 'desc', 'category', 'click_nums', 'address', 'city']
	list_filter = ['name', 'desc', 'category', 'click_nums', 'address', 'city', 'add_time']
	readonly_fields = ['click_nums', 'fav_nums', 'course_num', 'students']
	relfield_style = ['fk_ajax']


class TeacherAdmin(object):
	list_display = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nims',
	                'add_time']
	search_fields = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nims']
	list_filter = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nims',
	               'add_time']
	readonly_fields = ['click_nums', 'fav_nims']



xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
