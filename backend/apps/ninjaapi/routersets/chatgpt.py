from typing import List, Dict

import bs4
import requests
from pydantic.networks import HttpUrl
from loguru import logger

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, StreamingHttpResponse
from ninja import Router, Form

from . import utils

router = Router(tags=["chatgpt"])


@router.post("/ask_ai_one_question", summary="问 ai 一个问题")
def ask_ai_one_question(request: WSGIRequest, prompt: str = Form(max_length=1000)):
    # doc: 问 ai 一个问题
    message = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    return utils.get_ai_event_steam_response(message)


@router.post("/ask_english_ai", summary="问 英语学习 ai")
def ask_english_ai(request: WSGIRequest, prompt: str = Form(max_length=1000)):
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
def ask_function_naming_ai(request: WSGIRequest, prompt: str = Form(max_length=1000)):
    prompt = """
        你是一个专业程序员，我有一个功能为：{prompt} 的函数，请帮我命名。
        要求：你的回复只能是一个 json 列表，使用蛇形命名法（markdown 的相关内容也不需要）
    """.format(prompt=prompt)
    message = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    return utils.get_ai_event_steam_response(message)


@router.post("/ask_variable_naming_ai", summary="问 变量命名 ai")
def ask_variable_naming_ai(request: WSGIRequest, prompt: str = Form(max_length=1000)):
    prompt = """
        你是一个专业程序员，我有一个功能为：{prompt} 的变量名，请帮我命名。
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
def english_translation_and_grammar_analysis(request: WSGIRequest, raw_prompt: str = Form(max_length=1000)):
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


def get_text_of_html(html_content: str):
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    return soup.get_text(strip=False)  # strip=True 会去除空白符


@router.post("/summarize_url_content", summary="ai 总结网址信息")
def summarize_url_content(request: WSGIRequest, url: Form[HttpUrl]):
    # todo: 很多网站都需要登录怎么解决？
    #  涉及爬虫技术 -> requests, lxml, Beautiful Soup, Scrapy, Selenium, Pandas, Puppeteer, Requests-HTML,

    # [tip] 此处可以对接第三方服务，现在就有的自动搜索服务
    response = requests.get(url, verify=False)
    http_content = response.content.decode("utf-8")
    content = get_text_of_html(http_content)

    message = [
        {
            "role": "user",
            "content": "请帮我将下面的文章内容用中文总结一下\n\n{prompt}".format(prompt=content)
        }
    ]
    return utils.get_ai_event_steam_response(message)
