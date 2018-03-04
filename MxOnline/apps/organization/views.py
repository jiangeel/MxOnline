import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from operation.models import UserFavorite
from courses.models import Course
from .models import CourseOrg, CityDict, Teacher
from django.shortcuts import render_to_response
from .forms import UserAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

class IndexView(View):
    """首页"""
    def get(self, request):

        some_courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]

        some_orgs = CourseOrg.objects.filter()[:25]
        return render(request, 'index.html', {
            'some_courses': some_courses,
            'banner_courses': banner_courses,
            'some_orgs': some_orgs

        })


class OrgView(View):
    """课程机构列表"""
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        host_orgs = all_orgs.order_by("-click_nums")[:3]
        all_cities = CityDict.objects.all()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                            Q(desc__icontains=search_keywords)
                                        )

        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort", "")
        if sort == "student":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")


        org_nums = all_orgs.count()

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "host_orgs": host_orgs,
            "sort": sort
        })

class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 本身可以直接save(),而不需要一个一个实例化
            user_ask = userask_form.save(commit=True)
            # ajax 异步操作，返回json
            # msg_dict = {}
            return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'fail', 'msg': '添加出错'}), content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })



class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()


        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 15, request=request)
        course = p.page(page)

        return render(request, 'org-detail-course.html', {
            'all_courses': course,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav

        })


class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav

        })

class OrgTeacherView(View):
    """
    机构中的讲师列表页
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 对教师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav

        })

class AddFavView(View):
    """
    用户收藏以及取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", "")

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '请先登录'}), content_type='application/json')

        exit_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=fav_type)
        # 记录已经存在， 则取消收藏
        if exit_records:
            exit_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type='application/json')

            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}), content_type='application/json')

class TeacherListView(View):
    """顶层授课教师页面"""
    def get(self, request):
        all_teachers = Teacher.objects.all()

        hot_teachers = Teacher.objects.all().order_by('-exp')
        teacher_count = Teacher.objects.all().count()

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = Teacher.objects.all().order_by('-fans')

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(teacher_name__icontains=search_keywords) |
                                       Q(teacher_desc__icontains=search_keywords)
                                       )

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)

        return render(request, 'teacher-list.html', {
            'all_teachers': all_teachers,
            'hot_teachers': hot_teachers[:10],
            'sort': sort,
            'teacher_count': teacher_count
        })

class TeacherDetailView(View):
    """教师详情页"""
    def get(self, requests, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))

        hot_teachers = Teacher.objects.all().order_by('-fans')

        return render(requests, 'teacher-detail.html', {
            'teacher': teacher,
            'hot_teachers': hot_teachers[:5]
        })