from django import forms
from rest_framework import serializers  # 导入序列化器

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'introduction', 'teacher', 'price')
