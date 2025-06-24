from typing import List, Dict

import requests
from loguru import logger

from django.http import StreamingHttpResponse


def get_ai_event_steam_response(message: List[Dict], mode: str = "gpt4_o_mini"):
    # doc: 获取 ai 的 event stream 响应
    url = "https://aliyun.zaiwen.top/admin/chatbot"
    data = {
        "message": message,
        "mode": mode,
        "prompt_id": "",
        "key": None
    }
    proxies = None

    def event_stream():
        # todo: 不要使用 verify=False，需要解决这个问题
        with requests.post(url, json=data, stream=True, timeout=300, proxies=proxies, verify=False) as response:
            logger.info(f"[get_ai_event_steam_response] response.status_code: {response.status_code}")
            for line in response.iter_lines():
                if not line:
                    continue
                yield line.decode("utf-8") + "\n"

    # 2024-12-13-00:10：测试发现，没什么问题。但是前端没有建立 EventStream，Swagger UI 本身无法连接到 SSE！
    event_stream_generator = event_stream()
    response = StreamingHttpResponse(event_stream_generator, content_type="text/event-stream")
    # 关闭缓存
    response["Cache-Control"] = "no-cache"
    return response
