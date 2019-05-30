from toga_wpf.base import Widget
from toga_wpf.libs import Controls


class Label(Widget):
    def create(self):
        self.native = Controls.Label()

    def set_text(self, value: object) -> None:
        self.native.Content = value
