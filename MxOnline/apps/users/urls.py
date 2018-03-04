# -*-coding=utf-8-*-
__author__ = 'Eeljiang'
__date__ = '09/02/2018 21:20'


from django.conf.urls import url, include
from .views import UserInfoView, MyCoursesView, MessageView, MyFavCourse, MyFavOrg, MyFavTeacher
urlpatterns = [
    # 机构列表
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    url(r'^mycourses/$', MyCoursesView.as_view(), name="user_mycourses"),
    url(r'^message/$', MessageView.as_view(), name="user_message"),
    url(r'^favorg/$', MyFavOrg.as_view(), name="user_fav_org"),
    url(r'^favteacher/$', MyFavTeacher.as_view(), name="user_fav_teacher"),
    url(r'^favcourse/$', MyFavCourse.as_view(), name="user_fav_course"),

    # url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    # url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    # url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    # url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    # url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    # url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),


]