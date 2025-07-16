from django import forms

from .models import Task


# ModelForm，根据 Django 模型自动生成表单
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


# Form，需要自定义表单中的字段
class TaskFileUploadForm(forms.Form):
    # error_message = forms.Textarea()
    error_message = forms.CharField(label="错误信息",
                                    max_length=1000,
                                    # 定义表单 error_message 字段的输入控件为 Textarea，还指定了其样式 css。
                                    widget=forms.Textarea(
                                        attrs={'class': 'custom'},
                                    ),
                                    error_messages={
                                        "required": "错误信息不能为空",
                                    })
    contact = forms.CharField(label="联系方式", max_length=20)
    file = forms.FileField(label="附件上传")
