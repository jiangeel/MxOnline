# -*-coding=utf-8-*-
__author__ = 'Eeljiang'
__date__ = '08/02/2018 14:12'


from django.conf.urls import url, include
from .views import CourseView, CourseDetailView, CourseVideoView, CourseCommentView, CourseAddCommentView, CourseStartLearnView, CoursePlayView
urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseView.as_view(), name="courses_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment/$', CourseAddCommentView.as_view(), name="course_add_comment"),
    url(r'^start_learn/$', CourseStartLearnView.as_view(), name="course_start_learn"),
    url(r'^play/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="course_play"),

]