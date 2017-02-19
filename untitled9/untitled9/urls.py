from django.conf.urls import url, include
import xadmin
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetPasswordView, ModifyPWDView, LogoutView, IndexView
from untitled9.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget', ForgetView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetPasswordView.as_view(), name='password_reset'),
    url(r'^modify_pwd/$', ModifyPWDView.as_view(), name='password_modify'),
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    url(r'^org/', include('organization.urls', namespace='org')),

    url(r'^course/', include('courses.urls', namespace='course')),

    url('^user/', include('users.urls', namespace='user')),

    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'














