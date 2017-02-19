# _*_ coding: utf-8 _*_
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'fzk'
__date__ = '2017/2/9 0009 15:12'


class LoginRequiredMixin(object):

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)