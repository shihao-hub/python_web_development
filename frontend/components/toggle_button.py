"""
视图尝试一下定制化

"""

from nicegui import ui


class ToggleColorButton(ui.button):
    """具有内部布尔状态的红/绿切换按钮"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state = False
        self.on('click', self.toggle)

    def toggle(self) -> None:
        """Toggle the button state."""
        self._state = not self._state
        self.update()

    def update(self) -> None:
        self.props(f'color={"green" if self._state else "red"}')
        super().update()


if __name__ in {"__main__", "__mp_main__"}:
    ToggleColorButton('Toggle me')

    ui.run(host="localhost", port=10086, reload=False, show=False, favicon="🚀")
