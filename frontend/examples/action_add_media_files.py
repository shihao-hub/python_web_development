from loguru import logger

import requests
from nicegui import app, ui
from pathlib import Path

# todo: 确定一下，好特别。
#       我目前猜测，启动的时候就是完全后端代码执行，ui.video 等只不过是注册组件，生成 html css js 返回给客户端。（templates）

media = Path('media')
media.mkdir(exist_ok=True)
r = requests.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
(media / 'clouds.mp4').write_bytes(r.content)
app.add_media_files('/my_videos', media)
ui.video('/my_videos/clouds.mp4')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
