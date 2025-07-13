from typing import List, Dict

from schema import Schema
from loguru import logger

from django.db import models, transaction


class ErrorFeedbackInfo(models.Model):
    """错误反馈信息"""

    id = models.AutoField(primary_key=True)

    error_scenario = models.CharField(verbose_name="错误场景")
    contact = models.CharField(verbose_name="联系方式")
    filepaths = models.JSONField(verbose_name="附件路径")


class ModInfo(models.Model):
    """模组信息"""

    id = models.AutoField(primary_key=True)

    name = models.CharField(verbose_name="模组名称", max_length=255)
    description = models.TextField(verbose_name="模组描述")
    author = models.CharField(verbose_name="模组作者", max_length=255)
    # todo: 实现一个 ListStringField，提供序列化和反序列化对应接口实现应该就可以了
    tags = models.JSONField(verbose_name="模组标签", default=list, help_text="字段格式：[ str, str , ... ]")
    version = models.CharField(verbose_name="模组版本", max_length=255, null=True)
    url = models.URLField(verbose_name="模组下载链接", null=True)

    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="是否删除", default=False)

    @classmethod
    def mock_init_data(cls):
        """mork 的初始数据，进行创建或更新操作"""
        mork_items = [
            dict(name="更多物品", description="新增 80+ 种物品，涵盖装备、建筑等方面。", author="心悦卿兮",
                 tags=["联机", "物品", "辅助"]),
            dict(name="宠物增强", description="修改原版宠物", author="心悦卿兮", tags=["联机"]),
            dict(name="复活按钮和传送按钮", description="无", author="心悦卿兮", tags=["联机"]),
            dict(name="便携大箱子", description="无", author="心悦卿兮", tags=["联机"]),
        ]
        with transaction.atomic():
            for obj_dict in mork_items:
                cls.objects.update_or_create(defaults=obj_dict, name=obj_dict["name"])
        logger.debug("创建 Mork 数据成功：{}", [e["name"] for e in mork_items])

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
        }


class ModItemInfo(models.Model):
    """模组物品信息"""

    id = models.AutoField(primary_key=True)

    image = models.FilePathField(verbose_name="图片路径", max_length=100, null=True)
    name = models.CharField(verbose_name="物品名称", max_length=20, unique=True)
    description = models.CharField(verbose_name="物品描述", max_length=1000)

    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="是否删除", default=False)

    # todo: 深入一下数据库及数据库涉及（诸如外键等知识）
    belonging_mod = models.ForeignKey(
        "ModInfo",
        verbose_name="所属模组",
        on_delete=models.CASCADE,
        related_name="mod_item_info",
    )

    @staticmethod
    def parse_items_from_file(filepath: str) -> List[Dict]:
        """解析指定文件，获得模组物品信息列表"""
        return []

    @classmethod
    def batch_update_or_create(cls, items: List[Dict]):
        """批量更新或创建"""
        # todo: 推荐这个 Schema 与 Pydantic/FastAPI 的 Schema 对比一下
        ModItemInfoSchema = Schema({

        })

        with transaction.atomic():
            for item in items:
                cls.objects.update_or_create(
                    defaults=item,
                    name=item["name"],
                )

# todo: 模组的物品信息必须要存在数据库里，大不了每次 git push 的适合预先序列化 sql 文件再一起 push 上去
#       还需要增加一个后台管理系统，主要用来方便地增加某个模组的物品信息
#       关于模组信息我选择用 json 文件，这时候需要考虑一下某个解析 json 文件并提供查询等功能的第三方库了！
#       （技术视野的重要性，技术调研的重要性，ai 提供了便捷的技术调研途径）

# todo: 模组物品介绍信息的数据流：.lua -> python lua -> sqlite.exe -> python -> .md
#       （这也是数据处理！！！）
