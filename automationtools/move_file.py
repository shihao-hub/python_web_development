"""
### 需求描述
将计算机文档目录下的最新创建的 .md 文件复制到 docs 目录中，
如果存在重名则移动失败。
如有余力，请处理更多的异常情况，并基于清晰的用户提示。

"""
import os
import shutil
from pathlib import Path

from loguru import logger


def get_documents_path() -> Path:
    """获取当前用户的文档路径（跨平台）"""
    # Windows 系统
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes

        # 调用系统 API 获取文档路径
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
        return Path(buf.value)

    # macOS 和 Linux 系统
    else:
        # 尝试获取 XDG_DOCUMENTS_DIR 环境变量
        xdg_docs = os.environ.get('XDG_DOCUMENTS_DIR')
        if xdg_docs:
            return Path(xdg_docs)

        # 回退到主目录下的 Documents 文件夹
        return Path.home() / 'Documents'


host_document_path = get_documents_path()

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = Path(host_document_path)
TARGET_PATH = ROOT_DIR / "docs"

if not TARGET_PATH.exists():
    raise FileNotFoundError(f"目标目录 {TARGET_PATH} 不存在")

files = list(SOURCE_PATH.glob("*.md"))
files = sorted(files, key=lambda x: x.stat().st_mtime)
# logger.debug("{}", files)
if len(files) == 0:
    raise FileNotFoundError("未找到任何 .md 文件")
file = files[-1]
file_name = file.name
target_file = TARGET_PATH / file_name
if target_file.exists():
    raise FileExistsError(f"文件 {file_name} 已存在，复制失败")

try:
    # 复制文件（保留文件名）
    shutil.copy(SOURCE_PATH / file_name, target_file)
    # todo: 并将其假如到 git 中
    logger.info(f"复制文件 {file_name} 成功")
except Exception as e:
    logger.error(f"复制文件 {file_name} 失败，原因：{e}")
