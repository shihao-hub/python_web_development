from nicegui import Tailwind, ui

ui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')
ui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')

# NiceGUI 提供了一个流畅的、支持自动补全的界面，用于向 UI 元素添加 Tailwind 类。
# todo: 该文档应该翻译自官方文档，唉，可惜英语不好，所以我认为，英语至少占据前期计算机学习的 40%+ 的比重！
#       去看文档！！！

red_style = Tailwind().text_color('red-600').font_weight('bold')
label_c = ui.label('Label C')
red_style.apply(label_c)
ui.label('Label D').tailwind(red_style)

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
