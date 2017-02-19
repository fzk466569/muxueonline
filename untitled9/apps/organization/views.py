# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http.response import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course

# Create your views here.


class OrgView(View):
	def get(self, request):
		all_orgs = CourseOrg.objects.all()
		all_citys = CityDict.objects.all()

		hot_orgs = all_orgs.order_by('-click_nums')[0:3]

		#城市筛选
		city_id = request.GET.get('city', '')
		if city_id:
			all_orgs = CourseOrg.objects.filter(city_id=int(city_id))

		#机构类别
		category=request.GET.get('ct', '')
		if category:
			all_orgs = all_orgs.filter(category=category)

		#keywords
		search_keywords = request.GET.get('keywords','')
		if search_keywords:
			all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
										Q(brief__icontains=search_keywords) |
										Q(desc__icontains=search_keywords))

		sort=request.GET.get('sort', '')
		if sort:
			if sort == 'students':
				all_orgs = all_orgs.order_by('-students')
			elif sort == 'courses':
				all_orgs = all_orgs.order_by('-course_num')

		orgs_nums = all_orgs.count()

		#翻页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_orgs, 4, request=request)
		page_orgs = p.page(page)
		return render(request,'org-list.html', {
			'page_orgs': page_orgs,
			'all_citys': all_citys,
			'orgs_nums': orgs_nums,
			'city_id': city_id,
			'category': category,
			'hot_orgs': hot_orgs,
			'sort': sort,
			})


class AddUserAskView(View):
	def post(self, request):
		userask_form=UserAskForm(request.POST)
		if userask_form.is_valid():
			user_ask=userask_form.save(commit=True)
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
	def get(self, request, org_id):
		current_page = 'home'
		course_org = CourseOrg.objects.get(id=int(org_id))
		course_org.click_nums += 1
		course_org.save()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
				has_fav = True
		all_courses = course_org.course_set.all()[:3]
		all_teachers = course_org.teacher_set.all()[:1]
		return render(request, 'org-detail-homepage.html', {
			'all_teachers': all_teachers,
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav
		})


class OrgDescView(View):
	def get(self, request,org_id):
		current_page = 'desc'
		course_org = CourseOrg.objects.get(id=int(org_id))
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
				has_fav = True
		return render(request, 'org-detail-desc.html', {
			'current_page': current_page,
			'course_org': course_org,
			'has_fav': has_fav
		})


class OrgCourseView(View):
	def get(self, request, org_id):
		current_page = 'course'
		course_org = CourseOrg.objects.get(id=int(org_id))
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
				has_fav = True
		all_courses = course_org.course_set.all()
		return render(request, 'org-detail-course.html', {
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav
		})


class OrgTeacherView(View):
	def get(self, request, org_id):
		current_page = 'teacher'
		course_org = CourseOrg.objects.get(id=int(org_id))
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
				has_fav = True
		all_teacher = course_org.teacher_set.all()
		return render(request, 'org-detail-teachers.html', {
			'current_page': current_page,
			'course_org': course_org,
			'all_teacher': all_teacher,
			'has_fav': has_fav
		})


class AddFavView(View):
	'''收藏及取消'''
	def post(self, request):
		fav_id = request.POST.get('fav_id', 0)
		fav_type = request.POST.get('fav_type', 0)

		if request.user.is_authenticated():
			exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
			if exist_records:
				'如果记录已经存在，表示用户想取消收藏'
				exist_records.delete()
				if int(fav_type) == 1:
					course = Course.objects.get(id=int(fav_id))
					course.fav_nums -= 1
					course.save()
				elif int(fav_type) == 2:
					teacher = Teacher.objects.get(id=int(fav_id))
					teacher.fav_nims -= 1
					teacher.save()
				elif int(fav_type) == 3:
					course_org = CourseOrg.objects.get(id=int(fav_id))
					course_org.fav_nums -= 1
					course_org.save()

				return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
			else:
				user_fav = UserFavorite()
				if int(fav_id) > 0 and int(fav_type) > 0:
					user_fav.user = request.user
					user_fav.fav_id = int(fav_id)
					user_fav.fav_type = int(fav_type)
					user_fav.save()

					if int(fav_type) == 1:
						course = Course.objects.get(id=int(fav_id))
						course.fav_nums -= 1
						if course.fav_nums < 0:
							course.fav_nums = 0
						course.save()
					elif int(fav_type) == 2:
						teacher = Teacher.objects.get(id=int(fav_id))
						teacher.fav_nims -= 1
						if teacher.fav_nims < 0:
							teacher.fav_nims = 0
						teacher.save()
					elif int(fav_type) == 3:
						course_org = CourseOrg.objects.get(id=int(fav_id))
						course_org.fav_nums -= 1
						if course_org.fav_nums < 0:
							course_org.fav_nums = 0
						course_org.save()

					return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":"用户未登陆"}', content_type='application/json')


class TeacherListView(View):
	def get(self, request):
		all_teacher = Teacher.objects.all()
		all_teacher_num = Teacher.objects.all().count()

		recommend_teacher = all_teacher.order_by('-click_nums')[:5]

		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'hot':
				all_teacher = all_teacher.order_by('-click_nums')

		search_keywords = request.GET.get('keywords', '')
		if search_keywords:
			all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) |
											Q(work_position__icontains=search_keywords) |
											Q(work_company__icontains=search_keywords))

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_teacher, 4, request=request)
		page_teacher = p.page(page)

		return render(request, 'teachers-list.html', {
			'page_teacher': page_teacher,
			'recommend_teacher': recommend_teacher,
			'all_teacher_num': all_teacher_num,
		})


class TeacherDetailView(View):
	def get(self, request, teacher_id):
		teacher = Teacher.objects.get(id=int(teacher_id))
		teacher.click_nums += 1
		teacher.save()
		organization = CourseOrg.objects.get(id=teacher.org_id)
		recommend_teacher = Teacher.objects.all().order_by('-click_nums')[:5]
		courses = teacher.course_set.all()

		has_teacher_fav = False
		has_org_fav = False
		if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.id):
			has_teacher_fav = True

		if UserFavorite.objects.filter(user=request.user,fav_type=3, fav_id=teacher.org.id):
			has_org_fav = True
		return render(request, 'teacher-detail.html', {
			'teacher': teacher,
			'organization': organization,
			'recommend_teacher': recommend_teacher,
			'courses': courses,
			'has_teacher_fav': has_teacher_fav,
			'has_org_fav': has_org_fav
		})


