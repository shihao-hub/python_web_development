from loguru import logger

import logging
from datetime import datetime
from nicegui import ui

logger = logging.getLogger()


class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
        except Exception:
            self.handleError(record)


log = ui.log(max_lines=10).classes('w-full')
# logger.addHandler(LogElementHandler(log))
ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))

# fixme: 这个 ui.timer 里面真的会执行吗？会的。。有疑惑是因为 logger 默认情况下没有打印在控制台？
ui.timer(1, lambda: (
    logger.info("123"),
    print(123456)
))

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123", on_air=True)
