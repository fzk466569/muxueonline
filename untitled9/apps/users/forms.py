# _*_ coding: utf-8 _*_
from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile

__author__ = 'fzk'
__date__ = '2017/2/5 0005 19:59'


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=8)
	captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetPWDForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPWDForm(forms.Form):
	password1 = forms.CharField(required=True, min_length=8)
	password2 = forms.CharField(required=True, min_length=8)


class ImageUploadViewForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['image']


class UserInfoForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['nick_name', 'gender', 'address', 'mobile', 'birday']
