import json
from django.shortcuts import render
from django.http import HttpResponse


from utils.mixin_utils import LoginRequiredMixin

from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, Lesson, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from django.db.models import Q


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        # host_orgs = all_orgs.order_by("-click_nums")[:3]
        # all_cities = CityDict.objects.all()

        # 右侧推荐 按点击数
        hot_courses = all_courses.order_by("-students")[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(course_name__icontains=search_keywords) |
                                             Q(course_desc__icontains=search_keywords) |
                                             Q(course_introduction__icontains=search_keywords))


        # 排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_courses = all_courses.order_by("-fav_nums")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")



        # org_nums = all_orgs.count()

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 15, request=request)
        course = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": course,
            "hot_courses": hot_courses,
            # "all_cities": all_cities,
            # "org_nums": org_nums,
            # "city_id": city_id,
            # "category": category,
            # "host_orgs": host_orgs,
            "sort": sort
        })



class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.click_nums += 1

        course.save()

        has_learn = False
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


            if UserCourse.objects.filter(course_id=course.id, user=request.user):
                has_learn = True


        return render(request, 'course-detail.html', {
            'has_fav_course': has_fav_course,
            "has_fav_org": has_fav_org,
            'course': course,
            'has_learn': has_learn
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


class CourseVideoView(View):
    def get(self, request, course_id):
        # 当前是视频页还是评论页
        video_or_comment = "video"
        course = Course.objects.get(id=int(course_id))


        return render(request, 'course-video.html', {
            'course': course,
            'video_or_comment': video_or_comment

        })


class CourseCommentView(View):
    def get(self, request, course_id):
        # 当前是视频页还是评论页
        video_or_comment = "comment"
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course_id=int(course_id))

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_comments, 10, request=request)
        comments = p.page(page)

        return render(request, 'course-comment.html', {
            'course': course,
            'video_or_comment': video_or_comment,
            'all_comments': comments

        })

class CourseAddCommentView(View):
    def post(self, request):


        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '请先登录'}), content_type='application/json')

        comments = request.POST.get("comments", "")
        course_id = request.POST.get("course_id", "")
        course = Course.objects.get(id=int(course_id))

        if comments and course:
            coursecomments = CourseComments()
            coursecomments.user = request.user
            coursecomments.comments = comments
            coursecomments.course = course
            coursecomments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '评论成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '评论出错'}), content_type='application/json')



class CourseStartLearnView(View):
    def post(self, request):
        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '请先登录'}), content_type='application/json')

        course_id = request.POST.get("course_id", "")
        course = Course.objects.get(id=int(course_id))

        if not course:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '课程不存在'}), content_type='application/json')

        has_learn = UserCourse.objects.filter(course=int(course_id), user=request.user)
        if has_learn:
            return

        usercourse = UserCourse()
        usercourse.user = request.user
        usercourse.course = course
        usercourse.save()

        # 学习人数+1
        course.students += 1
        course.save()

        return HttpResponse(json.dumps({'status': 'success', 'msg': '已添加到学习单'}), content_type='application/json')


class CoursePlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        return render(request, 'course-play.html', {
            'course': course,
            'video': video
        })