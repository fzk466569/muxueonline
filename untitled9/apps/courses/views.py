# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, Video
from operation.models import CourseComments, UserFavorite, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
	def get(self, request):
		all_course = Course.objects.all().order_by('-add_time')
		hot_course = Course.objects.all().order_by('-add_time')[:3]

		search_keyword = request.GET.get('keywords', '')
		if search_keyword:
			all_course = all_course.filter(Q(name__icontains=search_keyword) |
											Q(tag__icontains=search_keyword) |
											Q(learn_about__icontains=search_keyword) |
											Q(youneed_knew__icontains=search_keyword))


		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'hot':
				all_course = all_course.order_by('-click_nums')
			elif sort == 'student':
				all_course = all_course.order_by('-student')

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_course, 6, request=request)
		page_course = p.page(page)

		return render(request, 'course-list.html', {
			'page_course': page_course,
			'hot_course': hot_course,
		})


class CourseDetailView(View):
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		course.click_nums += 1
		course.save()

		has_fav_org = False
		has_fav_course = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
				has_fav_course = True
			elif UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=3):
				has_fav_org = True
		tag = course.tag
		if tag:
			relate_courses = Course.objects.filter(tag=tag)[:2]
		else:
			relate_courses = []
		return render(request, 'course-detail.html', {
			'course': course,
			'relate_courses': relate_courses,
			'has_fav_course': has_fav_course,
			'has_fav_org': has_fav_org,
		})


class CourseInfoView(LoginRequiredMixin, View):
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		course.student += 1
		course.save()

		lessons = course.get_lessons()
		resources = course.get_course_resources()

		user_courses = UserCourse.objects.filter(user=request.user, course=course)
		if not user_courses:
			user_course = UserCourse(user=request.user, course=course)
			user_course.save()

		user_courses = UserCourse.objects.filter(course=course)
		user_ids = [user_course.user.id for user_course in user_courses]
		all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
		course_ids = [user_course.course.id for user_course in all_user_courses]
		relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

		return render(request, 'course-video.html', {
			'course': course,
			'lessons': lessons,
			'resources': resources,
			'relate_courses': relate_courses
		})


class CourseCommentView(LoginRequiredMixin, View):
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		comments = CourseComments.objects.all()
		resources = course.get_course_resources()

		tag = course.tag
		if tag:
			relate_courses = Course.objects.filter(tag=tag)[:2]
		else:
			relate_courses = []
		return render(request, 'course-comment.html', {
			'course': course,
			'comments': comments,
			'resources': resources,
			'relate_courses': relate_courses
		})


class AddCommentView(View):
	def post(self, request):

		if request.user.is_authenticated:
			course_id = request.POST.get('course_id', 0)
			comments = request.POST.get('comments', '')
			if course_id > 0 and comments:
				course_comment = CourseComments()
				course_comment.course = Course.objects.get(id=course_id)
				course_comment.id = course_id
				course_comment.comments = comments
				course_comment.user = request.user
				course_comment.save()
				return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
	def get(self, request, video_id):
		video = Video.objects.get(id=int(video_id))
		course = video.lesson.course
		course.student += 1
		course.save()

		lessons = course.get_lessons()
		resources = course.get_course_resources()

		user_courses = UserCourse.objects.filter(user=request.user, course=course)
		if not user_courses:
			user_course = UserCourse(user=request.user, course=course)
			user_course.save()

		user_courses = UserCourse.objects.filter(course=course)
		user_ids = [user_course.user.id for user_course in user_courses]
		all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
		course_ids = [user_course.course.id for user_course in all_user_courses]
		relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

		return render(request, 'course-play.html', {
			'course': course,
			'video': video,
			'lessons': lessons,
			'resources': resources,
			'relate_courses': relate_courses
		})







