from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Course


# todo: [to be attempted] inherit serializers.HyperlinkedModelSerializer
class CourseSerializer(serializers.ModelSerializer):
    # 外键字段、只读
    # todo: [to be understood] teacher.username 指的是对于表的 username 字段吗？
    # 对外键字段的序列化，可以指定遍历的深度。如果表结构有子表关联到父表，父表又关联到另外的父表，就可以设置深度。
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        # 注意元组中只有1个元素时不能写成("id")
        # exclude = ('id', )
        # fields = ('name', 'introduction', 'teacher', 'price')
        fields = "__all__"
        # 深度
        depth = 2


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
