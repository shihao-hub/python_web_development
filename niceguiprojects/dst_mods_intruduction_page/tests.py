from loguru import logger

import sqlalchemy as sa

from models import ModItemInfoModel
from utils import get_db, init_database

init_database()

with get_db() as db:
    info = ModItemInfoModel(image="home", name="超级牛铃", description="""
    - 超级牛铃
    """)
    db.add(info)
    db.commit()
