# -*-coding=utf-8-*-
__author__ = 'Eeljiang'
__date__ = '05/02/2018 19:20'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city']



class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position',
                    'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position',
                     'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position',
                   'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
