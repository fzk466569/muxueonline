# coding:utf-8
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetPWDForm, ModifyPWDForm, ImageUploadViewForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from users.models import Banner


class CustomBackend(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		from django.core.urlresolvers import reverse
		return HttpResponseRedirect(reverse("index"))


class LoginView(View):
	def get(self, request):
		return render(request, 'login.html', {})

	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				if user.is_active:
					login(request, user)
					from django.core.urlresolvers import reverse
					return HttpResponseRedirect(reverse('index'))
				else:
					return render(request, 'login.html', {'msg': u'用户未激活'})
			else:
				return render(request, 'login.html', {'msg': u'用户名或密码错误'})
		else:
			return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get('email', '')
			if UserProfile.objects.filter(email=user_name):
				return render(request, 'register.html', {'register_form': register_form, 'msg': u'用户已存在'})
			pass_word = request.POST.get('password', '')
			user_profile = UserProfile()
			user_profile.is_active = False
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.password = make_password(pass_word)
			user_profile.save()

			#注册成功写入欢迎注册消息
			user_message = UserMessage()
			user_message.user_id = user_profile.id
			user_message.message = u"欢迎注册慕学在线网"
			user_message.save()

			send_register_email(user_name, 'register')
			return render(request, 'login.html')
		else:
			return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
			return render(request, 'login.html')
		else:
			return render(request, 'active_fail.html')


class ForgetView(View):
	def get(self, request):
		forget_form = ForgetPWDForm(request.POST)
		return render(request, 'forgetpwd.html', {'forget_form': forget_form})

	def post(self, request):
		forget_form = ForgetPWDForm(request.POST)
		if forget_form.is_valid():
			email = request.POST.get('email', '')
			send_register_email(email, send_type='forget')
			return render(request, 'email_send_success.html')
		else:
			return render(request, 'forgetpwd.html')


class ResetPasswordView(View):
	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, 'password_reset.html', {'email': email})
		else:
			return render(request, 'active_fail.html')
		return render(request, 'login.html')


class ModifyPWDView(View):
	def post(self, request):
		modify_pwd_form = ModifyPWDForm(request.POST)
		if modify_pwd_form.is_valid():
			email = request.POST.get('email', '')
			password1 = request.POST.get('password1', '')
			password2 = request.POST.get('password2', '')
			if password1 == password2:
				user = UserProfile.objects.get(email=email)
				user.password = make_password(password1)
				user.save()
				return render(request, 'login.html')
			else:
				return render(request, 'password_reset.html', {'email': email, 'msg': u'两次密码不一致'})
		else:
			email = request.POST.get('email', '')
			return render(request, 'password_reset.html', {'email': email, 'modify_pwd_form': modify_pwd_form})


class UserInfoView(LoginRequiredMixin, View):
	def get(self, request):
		current_page = 'info'
		return render(request, 'usercenter-info.html', {
			'user': request.user,
			'current_pag': current_page
		})

	def post(self, request):
		user_info_form = UserInfoForm(request.POST, instance=request.user)
		if user_info_form.is_valid():
			user_info_form.save()
			return HttpResponse({'status': 'success'}, content_type='application/json')
		else:
			return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
	def post(self, request):
		image_form = ImageUploadViewForm(request.POST, request.FILES, instance=request.user)
		if image_form.is_valid():
			image_form.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail"}', content_type='application/json')


class ChangePWDView(LoginRequiredMixin, View):
	def post(self, request):
		modify_pwd_form = ModifyPWDForm(request.POST)
		if modify_pwd_form.is_valid():
			password1 = request.POST.get('password1', '')
			password2 = request.POST.get('password2', '')
			if password1 == password2:
				request.user.password = make_password(password1)
				request.user.save()
				return HttpResponse('{"status":"success"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail","msg":"两次密码输入不一致"}', content_type='application/json')
		else:
			return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendMailCodeView(LoginRequiredMixin, View):
	def get(self, request):
		email = request.GET.get('email', '')

		if UserProfile.objects.filter(email=email):
			return HttpResponse({'email': '此邮箱已经被绑定'}, content_type='application/json')
		send_register_email(email, 'reset_email')
		return HttpResponse({'status': 'success'}, content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
	def post(self, request):
		email = request.POST.get('email', '')
		code = request.POST.get('code', '')

		existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='reset_email')
		if existed_records:
			user = request.user
			user.email = email
			user.save()
			return HttpResponse({'status': 'success'}, content_type='application/json')
		else:
			return HttpResponse({'email': '验证码出错'}, content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
	def get(self, request):
		current_page = 'course'
		user_courses = UserCourse.objects.filter(user=request.user)
		return render(request, 'usercenter-mycourse.html', {
			'user_courses': user_courses,
			'current_pag': current_page
		})


class MyFavOrgView(LoginRequiredMixin, View):
	def get(self, request):
		current_page = 'fav'
		org_list = []
		fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=3)
		for fav_org in fav_orgs:
			org_id = fav_org.fav_id
			org = CourseOrg.objects.get(id=org_id)
			org_list.append(org)

		return render(request, 'usercenter-fav-org.html', {
			'org_list': org_list,
			'current_pag': current_page
		})


class MyFavTeacherView(LoginRequiredMixin, View):
	def get(self, request):
		current_page = 'fav'
		teacher_list = []
		fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=2)
		for fav_teacher in fav_teachers:
			teacher_list.append(Teacher.objects.get(id=fav_teacher.fav_id))

		return render(request, 'usercenter-fav-teacher.html', {
			'teacher_list': teacher_list,
			'current_pag': current_page
		})


class MyFavCourseView(LoginRequiredMixin, View):
	def get(self, request):
		current_page = 'fav'
		course_list = []
		fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
		for fav_course in fav_courses:
			course_list.append(Course.objects.get(id=fav_course.fav_id))

		return render(request, 'usercenter-fav-course.html', {
			'course_list': course_list,
			'current_pag': current_page
		})


class MyMessageView(LoginRequiredMixin, View):
	def get(self, request):
		current_pag = 'msg'
		all_message = UserMessage.objects.filter(user_id=request.user.id)
		all_unread_messages = UserMessage.objects.filter(user_id=request.user.id, is_read=False)
		for unread_message in all_unread_messages:
			unread_message.is_read = True
			unread_message.save()

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_message, 4, request=request)
		page_messages = p.page(page)
		return render(request, 'usercenter-message.html', {
			'page_messages': page_messages,
			'current_pag': current_pag
		})


class IndexView(View):
	#慕学在线网首页
	def get(self, request):
		all_banners = Banner.objects.all().order_by('index')
		all_courses = Course.objects.filter(is_banner=False)[:6]
		banner_courses = Course.objects.filter(is_banner=True)[:3]
		course_orgs = CourseOrg.objects.all()[:15]
		return render(request, 'index.html', {
			'all_banners': all_banners,
			'all_courses': all_courses,
			'banner_courses': banner_courses,
			'course_orgs': course_orgs
		})


def page_not_found(request):
	from django.shortcuts import render_to_response
	response = render_to_response('404.html', {})
	response.status_code = 404
	return response


def server_error(request):
	from django.shortcuts import render_to_response
	response = render_to_response('500.html', {})
	response.status_code = 500
	return response
