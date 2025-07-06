from nicegui import ui

# 显示一个视频，带控制条，自动播放但默认静音（以便浏览器允许自动播放）
ui.video('https://www.w3schools.com/html/mov_bbb.mp4').props('controls autoplay muted')

# 也可以让用户选择是否静音
ui.checkbox('静音', value=True, on_change=lambda e: video.run_js(f"el.muted = {str(e.value).lower()}"))

# 如果想要在页面显示更多提示
ui.label('这是一个示例视频，可以使用下方复选框切换静音。')

# 还可以直接获取 video 元素，设置更多参数
video = ui.video('https://www.w3schools.com/html/mov_bbb.mp4')

ui.run(host="localhost", port=13002, reload=False, show=False, favicon="🚀")
