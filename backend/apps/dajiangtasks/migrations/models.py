from django.db import models


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
