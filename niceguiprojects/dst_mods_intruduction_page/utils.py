import contextlib
import uuid
from pathlib import Path

import cachetools
from loguru import logger

from settings import ROOT_DIR, STATIC_DIR


class FileUploadError(Exception):
    pass


class FileUploadManager:
    """
    Usage:
        pass
    """

    def __init__(self):
        self._storage_path = ROOT_DIR / "storage" / "uploads"
        self._temp_storage_path = ROOT_DIR / "storage" / "temp_uploads"
        self._saved_file_size = 0
        self._max_file_size = 1024 * 1024 * 1024 * 10  # 10GB

    def _check_max_file_size(self, new_file_size: int):
        if self._saved_file_size + new_file_size > self._max_file_size:
            raise FileUploadError("文件大小超出限制")

    def _check_temp_dir_state(self):
        """检查临时目录的状态，并考虑是否要启动清除临时目录程序"""
        # 我有点无语，ui.upload 这么难用吗？

    def save(self,
             filecontent: bytes,
             file_extension: str,
             filename: str = None,
             is_temp: bool = False,  # 是否是临时文件
             ) -> Path:  # 返回文件路径
        """存储文件"""
        if filename is None:
            filename = str(uuid.uuid4()) + ("" if file_extension is None else file_extension)

        storage_path = self._storage_path

        if is_temp:
            storage_path = self._temp_storage_path
            self._check_temp_dir_state()

        filepath = storage_path / filename
        view = memoryview(filecontent)
        self._check_max_file_size(view.nbytes)
        self._saved_file_size += view.nbytes
        filepath.write_bytes(filecontent)
        logger.info("存储" + ("临时" if is_temp else "") + "文件成功，文件名：{}", filename)
        return filepath

    def delete(self, filename: str,
               is_temp: bool = False,  # 是否是临时文件
               ) -> bool:
        """删除文件"""
        storage_path = self._storage_path
        if is_temp:
            storage_path = self._temp_storage_path

        filepath = storage_path / filename
        if not filepath.exists() and filepath.is_dir():
            logger.warning("删除" + ("临时" if is_temp else "") + "文件失败，文件名：{}", filename)
            return False
        filepath.unlink()
        logger.info("删除" + ("临时" if is_temp else "") + "文件成功，文件名：{}", filename)
        return True

    class UnitTest:
        """暂时使用，单元测试与模块绑定"""

        def __init__(self):
            self.target: FileUploadManager = FileUploadManager()

        def test_save_and_delete(self):
            filename = str(uuid.uuid4())
            self.target.save(b"test", filename)
            # 预期结果：文件保存成功
            self.target.delete(filename)
            # 预期结果：文件删除成功


# @cachetools.cached(cachetools.TTLCache(maxsize=20, ttl=60 * 5))
def read_static_file(relative_path: str) -> str:
    """读取 static 文件"""
    filepath = ROOT_DIR / "static"
    for part in Path(relative_path).parts:
        filepath = filepath / part
    if not filepath.exists():
        raise FileNotFoundError(f"文件 `{relative_path}` 不存在")
    return filepath.read_text("utf-8")  # 进行了一层封装


# @cachetools.cached(cachetools.TTLCache(maxsize=20, ttl=60 * 5))
def read_markdown_file(relative_path: str):
    """读取 markdown 文件"""
    markdown_path = STATIC_DIR / "markdown" / Path(relative_path)
    return markdown_path.read_text("utf-8")
