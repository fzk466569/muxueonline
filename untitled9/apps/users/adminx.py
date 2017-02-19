# _*_ coding: utf-8 _*_

import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _

__author__ = 'fzk'
__date__ = '2017/2/4 0004 21:55'


class UserProfileAdmin(UserAdmin):
	def get_form_layout(self):
		if self.org_obj:
			self.form_layout = (
				Main(
					Fieldset('',
					         'username', 'password',
					         css_class='unsort no_title'
					         ),
					Fieldset(_('Personal info'),
					         Row('first_name', 'last_name'),
					         'email'
					         ),
					Fieldset(_('Permissions'),
					         'groups', 'user_permissions'
					         ),
					Fieldset(_('Important dates'),
					         'last_login', 'date_joined'
					         ),
				),
				Side(
					Fieldset(_('Status'),
					         'is_active', 'is_staff', 'is_superuser',
					         ),
				)
			)
		return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class GlobalSettings(object):
	site_title = u"慕学网后台管理系统 - 樊志魁"
	site_footer = u"欢迎来到本后台管理系统 - 樊志魁"
	menu_style = u"accordion"


class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
	list_display = ['title', 'image', 'url', 'index', 'add_time']
	search_fields = ['title', 'image', 'url', 'index']
	list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
