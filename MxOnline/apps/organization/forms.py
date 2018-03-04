# -*-coding=utf-8-*-
__author__ = 'Eeljiang'
__date__ = '07/02/2018 13:57'

import re

from django import forms
from operation.models import UserAsk


# 使用 model form
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        自定义对mobile是否合法进行验证
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号非法", code="mobile_invalid")

