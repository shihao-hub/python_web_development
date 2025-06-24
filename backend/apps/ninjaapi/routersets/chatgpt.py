from typing import List, Dict

import requests

from django.http import HttpRequest, StreamingHttpResponse
from ninja import Router, Form

from . import utils

router = Router(tags=["chatgpt"])


@router.post("/ask_ai_one_question", summary="问 ai 一个问题")
def ask_ai_one_question(request: HttpRequest, prompt: str = Form(max_length=1000)):
    # doc: 问 ai 一个问题
    message = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    return utils.get_ai_event_steam_response(message)


@router.post("/ask_english_ai", summary="问 英语学习 ai")
def ask_english_ai(request: HttpRequest, prompt: str = Form(max_length=1000)):
    # doc: 问 英语学习 ai
    init_prompt = """
        在接下来的对话中，你要帮助我学习英语。因为我的英语水平有限，所以拼写可能会不准确，如果语句不通顺，请猜测我要表达的意思。在之后的对话中，除了正常理解并回复我的问题以外，还要指出我说的英文中的语法错误和拼写错误。
        并且在以后的对话中都要按照以下格式回复:
        【翻译】此处将英文翻译成中文
        【回复】此处写你的正常回复
        【勘误】此处写我说的英文中的语法错误和拼写错误，如果夹杂汉字，请告诉我它的英文
        【提示】如果有更好或更加礼貌的英文表达方式，在此处告诉我如果你能明白并能够照做
        请说“我明白了”
    """
    # 使用经典同步
    message = [
        {
            "role": "user",
            "content": init_prompt
        },
        {
            "role": "assistant",
            "content": "我明白了。"

        },
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return utils.get_ai_event_steam_response(message)


@router.post("/ask_function_naming_ai", summary="问 函数命名 ai")
def ask_function_naming_ai(request: HttpRequest, prompt: str = Form(max_length=1000)):
    prompt = """
        我有一个功能为：{prompt} 的函数，请帮我命名。
        要求：你的回复只能是一个 json 列表，使用蛇形命名法（markdown 的相关内容也不需要）
    """.format(prompt=prompt)
    message = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    return utils.get_ai_event_steam_response(message)


@router.post("/english_translation_and_grammar_analysis", summary="英语翻译和语法分析")
def english_translation_and_grammar_analysis(request: HttpRequest, raw_prompt: str = Form(max_length=1000)):
    prompt = """
        对下面的内容进行翻译和语法分析：
        {prompt}
    """.format(prompt=raw_prompt)
    message = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    return utils.get_ai_event_steam_response(message)
