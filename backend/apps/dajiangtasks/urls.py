from django.urls import path

from . import views

# namespace
app_name = "dajiangtasks"

taskviews = views.TaskViews()

urlpatterns = [
    # 由于 django 最开始就是为了前后端不分离项目开发的，所以原始 django 并不适合前后端分离的 restful 接口开发（但是有 drf）
    # 但是 restful 风格的接口还是可以参考的（因为原始 django 适用于前后端不分离项目，所以 get post 等似乎没有明显地区分）
    # 收获：耦合严重，在我看来理解起来有些许困难啊，小项目都尚且如此。todo: 继续深入理解！
    path("list/", taskviews.task_list, name="task_list"),
    path("create/", taskviews.task_create, name="task_create"),
    path("delete/<int:pk>/", taskviews.task_delete, name="task_delete"),
    path("update/<int:pk>/", taskviews.task_update, name="task_update"),
    path("get/<int:pk>/", taskviews.task_detail, name="task_detail"),
]
