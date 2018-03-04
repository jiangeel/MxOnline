from datetime import datetime
from django.db import models

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(max_length=100, verbose_name="机构描述")
    category = models.CharField(max_length=4, choices=((("pxjg"), "培训机构"), ("gr", "个人"), ("gxjg", "高校机构")), verbose_name="机构类别", default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    image = models.ImageField(max_length=100, upload_to="course/%Y/%m", verbose_name="封面")
    city = models.ForeignKey(CityDict, verbose_name="所在城市", null=True, blank=True)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.IntegerField(verbose_name="教师ID", primary_key=True)

    teacher_name = models.CharField(max_length=50, verbose_name="教师名")
    image_url = models.CharField(max_length=200, verbose_name="头像", default="N")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    teacher_desc = models.TextField(verbose_name="教师介绍", default="N")
    exp = models.IntegerField(default=0, verbose_name="经验值")
    following = models.IntegerField(default=0, verbose_name="关注人数")
    fans = models.IntegerField(default=0, verbose_name="粉丝数")
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    # work_years = models.IntegerField(verbose_name="就职年限", default=10086)
    # work_company = models.CharField(max_length=50, verbose_name="就职公司", default="N")
    # click_nums = models.IntegerField(verbose_name="点击数", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def get_courses(self):
        all_courses = self.course_set.all().order_by('-score')
        return all_courses

    def __str__(self):
        return self.name