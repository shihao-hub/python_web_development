from django.db import models


# todo: 尝试弄明白 django orm 原理，甚至手搓一个支持 sqlite 的模仿 orm 一些功能的 orm 来！
#       在这个过程中：
#       1. 真正登堂入室了，因为阅读 python 源代码
#       2. sqlite 的 sql 语法可以足够熟悉，这对于数据库有很大的帮助
#       3. 学习和吸收 django 的精华

class Status(models.TextChoices):
    UNSTARTED = "u", "Not started yet"
    ONGOING = "o", "Ongoing"
    FINISHED = "f", "Finished"


class Task(models.Model):
    name = models.CharField(verbose_name="任务名", max_length=65, unique=True)
    status = models.CharField(verbose_name="任务状态", max_length=1, choices=Status.choices)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "app_dajiang_task"
        verbose_name = verbose_name_plural = "任务"
