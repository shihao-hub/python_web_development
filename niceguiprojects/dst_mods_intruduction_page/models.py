"""
sqlalchemy + sqlite.exe 实现数据库

"""
from typing import Dict, List

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from utils import Base


# todo: Base 实现好复杂，做了什么呢？
class ModItemInfoModel(Base):
    """模组物品信息"""
    __tablename__ = 'mod_item_infos'

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(100), comment="图片路径")
    name = Column(String(20), comment="物品名称", unique=True)  # todo: unique=True 中途添加后，为什么需要重建表才行？
    description = Column(String(1000), comment="物品描述")
    tags = Column(String(200), comment="物品标签", nullable=True)
    created_at = Column(DateTime, comment="创建时间", default=sa.func.now())
    updated_at = Column(DateTime, comment="更新时间", default=sa.func.now(), onupdate=sa.func.now())
    is_deleted = Column(Boolean, comment="是否删除", default=False)

    @staticmethod
    def parse_items_from_file(filepath: str) -> List[Dict]:
        """解析指定文件，获得模组物品信息列表"""
        return []

    @classmethod
    def batch_update_or_create(cls, db, items: List[Dict]):
        """批量更新或创建"""
        for item in items:
            db.query(cls).filter(cls.name == item["name"]).update(item, synchronize_session=False)
        db.commit()
