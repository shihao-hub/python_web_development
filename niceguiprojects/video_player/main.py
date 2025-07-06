from pathlib import Path

from loguru import logger

from nicegui import ui
from nicegui_toolkit.layout_tool import inject_layout_tool

# inject_layout_tool(ide="pycharm", language_locale="zh")

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"

# mock data test
# /query_video_info/
video_infos = [
    {
        "video_src": str(MEDIA_DIR / "13583325_3840_2160_24fps.mp4"),
        "username": "马桶的逗比狗生",
        "release_time": "2 周",
        "main_title": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "subtitle": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "like_count": 132
    },
]


def create_video_panel(video_info):
    with ui.column().classes("grid grid-rows-10 gap-0"):
        with ui.row().classes("row-span-6"):
            ui.video(video_info["video_src"], muted=False)
        # ui.space().classes("w-1")
        with ui.row().classes("row-span-1"):
            username = ui.label(text=video_info["username"])
            ui.space()
            release_time = ui.label(text=video_info["release_time"])
        with ui.column().classes("row-span-2 gap-y-0"):
            main_title = ui.label(text=video_info["main_title"]).classes("text-lg font-bold truncat")
            subtitle = ui.label(text=video_info["subtitle"]).classes("text-sm text-gray-500 mt-1")
        with ui.row().classes("row-span-1"):
            def handle_like_click():
                like.icon = "thumb_up_off_alt" if like.icon == "thumb_up" else "thumb_up"
                try:
                    if like.icon == "thumb_up":
                        like.text = str(int(like.text) + 1)
                    else:
                        like.text = str(int(like.text) - 1)
                except ValueError as e:
                    logger.error("{}", e)
                    ui.notify("出现出乎意料的操作，请联系开发人员", type="negative")

            def handle_dislike_click():
                dislike.icon = "thumb_down_off_alt" if dislike.icon == "thumb_down" else "thumb_down"

            like = ui.button(text="0", icon="thumb_up_off_alt", on_click=handle_like_click)
            dislike = ui.button(icon="thumb_down_off_alt", on_click=handle_dislike_click)


@ui.page("/")
def page():
    # 生成骨架和皮肤
    with ui.column().classes("mx-auto overflow-auto h-screen w-1/2"):
        for video_info in video_infos:
            create_video_panel(video_info)


ui.run(host="localhost", port=13002, reload=False, show=False, favicon="🚀")
