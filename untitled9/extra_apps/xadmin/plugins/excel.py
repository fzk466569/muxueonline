# _*_ coding: utf-8 _*_
# unfinished

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader

__author__ = 'fzk'
__date__ = '2017/2/11 0011 14:46'

class ListImportExcelPlugin(BaseAdminPlugin):
	import_excel = False

	def init_request(self, *args, **kwargs):
		return bool(self.import_excel)

	def block_top_toolbar(self, context, nodes):
		nodes.append(loader.render_to_string('xadmin/excel/model_list'))

xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)