"""MXOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve
from MXOnline.settings import MEDIA_ROOT
from organization.views import IndexView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index/$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # # 教师相关url配置
    # url(r'^teacher/', include('organization.urls', namespace="org")),

    # 课程相关url配置
    url(r'^courses/', include('courses.urls', namespace="courses")),

    # 个人中心相关url配置
    url(r'^usercenter/', include('users.urls', namespace="usercenter")),

    # 配置上传文件的处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT})

    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# 全局404配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
