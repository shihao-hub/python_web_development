"""
### 需求内容，在当前目录下通过 cmd 执行 git push origin master:main，不断重试直到成功

"""

import subprocess
import time

from loguru import logger


def git_push_with_retry():
    max_retries = 100  # 最大重试次数
    retry_delay = 5  # 每次重试间隔(秒)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"尝试第 {attempt} 次推送...")
            result = subprocess.run(
                ["git", "push", "origin", "master:main"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info("推送成功!")
            logger.info("{}", result.stdout)
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"推送失败: {e.stderr.strip()}")
            if attempt < max_retries:
                logger.info(f"{retry_delay}秒后重试...")
                time.sleep(retry_delay)

    logger.info(f"已达到最大重试次数 {max_retries}，推送失败")
    return False


if __name__ == "__main__":
    git_push_with_retry()
