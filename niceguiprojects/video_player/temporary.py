from pathlib import Path

from loguru import logger

from nicegui import ui

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"

# mock data
video_infos = [
    {
        "video_src": str(MEDIA_DIR / "13583325_3840_2160_24fps.mp4"),
        "username": "马桶的逗比狗生",
        "release_time": "2 周",
        "main_title": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "subtitle": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "like_count": 132
    },
    {
        "video_src": str(MEDIA_DIR / "mov_bbb.mp4"),
        "username": "马桶的逗比狗生",
        "release_time": "2 周",
        "main_title": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "subtitle": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "like_count": 132
    },
    {
        "video_src": "https://www.w3schools.com/html/mov_bbb.mp4",
        "username": "马桶的逗比狗生",
        "release_time": "2 周",
        "main_title": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "subtitle": "主人骗二哈去绝育，当二哈看到自己伤口后，大家千万憋住别笑",
        "like_count": 132
    },
]

for video_info in video_infos:
    # todo: 固定整块区域的宽度，否则不同视频源将有不同的大小，呃，前端好麻烦
    # 页面基础样式（全局字体、居中布局）
    with ui.element("div").style("""
        max-width: 850px; 
        margin: 20px auto; 
        font-family: '微软雅黑', Arial, sans-serif;
        padding: 0 15px;
    """).classes("overflow-auto"):
        # ------------------------------
        # 1. 图片区域（带文字 overlay）
        # ------------------------------
        with ui.element("div").style("position: relative; margin-bottom: 15px;"):
            # 图片（自适应宽度，圆角）
            # fixme: 为什么总是静音
            ui.video(video_info["video_src"]).style("width: 100%; border-radius: 12px;")
            # ui.video("https://www.w3schools.com/html/mov_bbb.mp4").style("width: 100%; border-radius: 12px;")

            # 图片中央的文字（绝对定位，居中）
            # ui.label("当二哈看到自己伤口后") \
            #     .style("""
            #         position: absolute;
            #         top: 50%;
            #         left: 50%;
            #         transform: translate(-50%, -50%);
            #         font-size: 26px;
            #         color: white;
            #         font-weight: bold;
            #         text-shadow: 2px 2px 6px rgba(0,0,0,0.7);  # 文字阴影（增强对比）
            #         text-align: center;
            #         padding: 0 20px;
            #     """)

        # ------------------------------
        # 2. 来源栏（红色图标+来源+时间）
        # ------------------------------
        with ui.row().style("justify-content: space-between; align-items: center; margin-bottom: 12px;"):
            # 左侧：红色图标+来源
            with ui.row().style("align-items: center; gap: 8px;"):
                # 红色小图标（带数字）
                ui.label("1") \
                    .style("""
                        background-color: #ff3d3d;
                        color: white;
                        padding: 3px 8px;
                        border-radius: 5px;
                        font-size: 12px;
                        font-weight: bold;
                    """)
                # 来源文字（灰色）
                ui.label(video_info["username"]) \
                    .style("color: #666; font-size: 14px;")

            # 右侧：时间（灰色）
            ui.label(video_info["release_time"]) \
                .style("color: #666; font-size: 14px;")

        # ------------------------------
        # 3. 标题与副标题
        # ------------------------------
        # 标题（加粗大字体）
        ui.label(video_info["main_title"]) \
            .style("""
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 8px;
                line-height: 1.4;
            """)

        # 副标题（灰色小字体，与标题内容重复）
        ui.label(video_info["subtitle"]) \
            .style("""
                color: #666;
                font-size: 15px;
                margin-bottom: 15px;
                line-height: 1.5;
            """)

        # ------------------------------
        # 4. 互动栏（点赞/踩）
        # ------------------------------
        with ui.row().style("align-items: center; gap: 30px; margin-bottom: 20px;"):
            def handle_like_click():
                like_icon.name = "thumb_up_off_alt" if like_icon.name == "thumb_up" else "thumb_up"
                try:
                    if like_icon.name == "thumb_up":
                        like_count.text = str(int(like_count.text) + 1)
                    else:
                        like_count.text = str(int(like_count.text) - 1)
                except ValueError as e:
                    logger.error("{}", e)
                    ui.notify("出现出乎意料的操作，请联系开发人员", type="negative")


            def handle_dislike_click():
                dislike_icon.name = "thumb_down_off_alt" if dislike_icon.name == "thumb_down" else "thumb_down"


            # 点赞（图标+数字）
            with ui.row().style("align-items: center; gap: 6px;"):
                like_icon = ui.icon("thumb_up_off_alt", color="#666", size="20px")  # 点赞图标
                like_icon.on("click", handle_like_click)
                like_count = ui.label(str(video_info["like_count"])).style("color: #666; font-size: 16px;")  # 点赞数

            # 踩（图标+数字）
            with ui.row().style("align-items: center; gap: 6px;"):
                dislike_icon = ui.icon("thumb_down_off_alt", color="#666", size="20px")  # 踩图标
                dislike_icon.on("click", handle_dislike_click)
                # ui.label("0").style("color: #666; font-size: 16px;")  # 踩数（原图未显示，用0代替）

ui.run(host="localhost", port=13002, reload=False, show=False, favicon="🚀")
