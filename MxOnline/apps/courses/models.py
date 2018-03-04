from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="课程ID")
    url = models.CharField(max_length=200, verbose_name="课程链接")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    students = models.IntegerField(default=1, verbose_name="学习人数")
    degree = models.CharField(max_length=2, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name="课程难度")
    learn_times = models.IntegerField(default=1, verbose_name="学习时长（分钟数）")
    score = models.FloatField(default=1, verbose_name="综合评分")
    course_desc = models.TextField(verbose_name="课程描述", default="N")
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name="课程教师", default=None)
    should_know = models.TextField(verbose_name="学前需知", default='N')
    can_learn = models.TextField(verbose_name="此课能学", default='N')
    category = models.CharField(max_length=50, verbose_name="课程类别", default="无")
    course_img = models.CharField(max_length=200, verbose_name="封面")
    course_introduction = UEditorField(verbose_name="课程详情", width=600, height=300,
                          imagePath='courses/ueditor/',
                          filePath='courses/ueditor/',
                          default='')
    course_label = models.CharField(max_length=20, default="", verbose_name="课程标签")
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, default=None)
    fav_nums = models.IntegerField(verbose_name="收藏人数")
    click_nums = models.IntegerField(verbose_name="点击数")
    is_banner = models.BooleanField(default=False, verbose_name="首页轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_lesson_nums(self):
        return self.lesson_set.all().count()
    # 在admin显示的动态数据标目
    get_lesson_nums.short_description = "章节数"


    # 在admin添加自定义的html链接
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='https://www.baidu.com'>跳转</>")
    go_to.short_description = "跳转"


    #获取本课程的所有章节
    def get_lessons(self):
        return self.lesson_set.all()

    def get_learn_users(self):
        s = self.usercourse_set.all()[:5]
        return s

    # 获取本课程的所有资源文件
    def get_resources(self):
        return self.courseresource_set.all()

    # 获取具有相同tag的相关课程
    def get_related_courses(self):
        related_courses = Course.objects.filter(course_label=self.course_label)

        # 排除本课程
        related_courses = related_courses.exclude(course_name=self.course_name)

        return related_courses[:3]



    # 获取学过该课程的学生的其他课程
    def get_also_learned_courses(self):
        all_usercourses = self.usercourse_set.all()

        also_learned_usercourses = [usercourse.user.usercourse_set.all() for usercourse in all_usercourses]

        courses = set(usercourse.course for also_learned_usercourse in also_learned_usercourses for usercourse in also_learned_usercourse)

        # courses.remove(self)

        courses = list(courses)

        return courses[:3]

    def __str__(self):
        return '{0}'.format(self.course_name)


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        # 不设置proxy的话会再生成一张表
        proxy = True


class Lesson(models.Model):
    lesson_id = models.IntegerField(primary_key=True, verbose_name="章节ID")
    course = models.ForeignKey(Course, verbose_name="课程")
    lesson_name = models.CharField(max_length=200, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    # 获取本章节的所有视频
    def get_videos(self):
        all_videos = self.course.video_set.all()
        videos = []
        for video in all_videos:
            if video.video_name.split('-')[0] == self.lesson_name[1]:
                if not videos or videos[0].video_name != video.video_name:
                    videos.append(video)
        return videos

    def __str__(self):
        return '{0}'.format(self.lesson_name)


class Video(models.Model):
    video_id = models.IntegerField(primary_key=True, verbose_name="视频ID")
    course = models.ForeignKey(Course, verbose_name="课程")
    video_name = models.CharField(max_length=200, verbose_name="视频名")
    video_url = models.CharField(max_length=200, default="N", verbose_name="视频链接")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.video_name)


class CourseResource(models.Model):
    Course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(max_length=100, upload_to="course/resource/%Y/%m", verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "资源文件"
        verbose_name_plural = verbose_name


