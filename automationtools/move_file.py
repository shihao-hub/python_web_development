"""
### 需求描述
将计算机文档目录下的最新创建的 .md 文件复制到 docs 目录中，
如果存在重名则移动失败。
如有余力，请处理更多的异常情况，并基于清晰的用户提示。

"""

import shutil
from pathlib import Path

from loguru import logger

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = Path(r"C:\Users\29580\Documents")
TARGET_PATH = ROOT_DIR / "docs"

if not TARGET_PATH.exists():
    raise FileNotFoundError(f"目标目录 {TARGET_PATH} 不存在")

files = list(SOURCE_PATH.glob("*.md"))
files = sorted(files, key=lambda x: x.stat().st_mtime)
# logger.debug("{}", files)
file = files[-1]
file_name = file.name
target_file = TARGET_PATH / file_name
if target_file.exists():
    raise FileExistsError(f"文件 {file_name} 已存在，复制失败")

try:
    # 复制文件（保留文件名）
    shutil.copy(SOURCE_PATH / file_name, target_file)
    logger.info(f"复制文件 {file_name} 成功")
except Exception as e:
    logger.error(f"复制文件 {file_name} 失败，原因：{e}")
