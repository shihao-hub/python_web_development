from loguru import logger

from djangoorm import load_djangoorm
from djangoorm.app.models import User

load_djangoorm()

User.objects.create(name="张三")
users = User.objects.all()
logger.debug("{}", users)
logger.debug("{}", users[0].name)
