from nicegui import ui


@ui.page("/")
def page_index():
    # [note] ui.element 似乎就是原始的标签，除了继承所在元素的属性外，不会有额外属性
    # [note] ui.label 居然就是原始 div，它的作用似乎就是文本的作用？毕竟元素的 _text 是私有的。
    with ui.header().classes("text-sm flex items-center px-4 py-3 bg-gray-900 justify-between"):
        # 左侧的图标和输入框
        with ui.element("div").classes("flex items-center text-white space-x-4"):
            with ui.link().classes("w-6 fill-current hover:text-gray-200"):
                ui.html("""
                    <svg height="32" aria-hidden="true" viewBox="0 0 24 24" version="1.1" width="32" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                        <path d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"></path>
                    </svg>
                    """)
            with ui.element("div").classes("relative"):
                ui.input(placeholder="Search or jump to ...").classes("""
                    rounded bg-gray-900 border border-gray-600 w-72 px-3 py-1
                    """)
                with ui.element("div").classes("absolute top-0 right-0 flex items-center h-full"):
                    with ui.element("div").classes("border border-gray-600 rounded text-xs text-gray-400 px-2 mr-2"):
                        ui.label("/")

            # 偏中间的横向列表（类似 ui.tabs 那样的）
            with ui.element("ul").classes("flex items-center font-semibold space-x-4"):
                # todo: 去除 ui.link 的下划线和修改默认的蓝色字体（疑问：nicegui 为什么没有提供清楚 element 默认值的功能？）
                with ui.element("li"):
                    with ui.element("a").classes("hover:text-gray-400"):
                        ui.label("Pull requests")
                with ui.element("li"):
                    ui.link("Issues").classes("hover:text-gray-400")
                with ui.element("li"):
                    ui.link("Marketplace").classes("hover:text-gray-400")
                with ui.element("li"):
                    ui.link("Explore").classes("hover:text-gray-400")

        with ui.element("div").classes("text-white"):
            ui.label("right")


if __name__ == '__main__':
    ui.run(title="模仿 github 主页", host="localhost", port=15003, dark=False, reload=False, show=False,
           storage_secret="NOSET")
