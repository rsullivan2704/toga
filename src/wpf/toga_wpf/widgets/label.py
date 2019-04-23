from .base import Widget
from toga_wpf.libs import WPF


class Label(Widget):
    def create(self):
        self.native = WPF.Controls.Label()

    def set_text(self, value: object) -> None:
        self.native.Content = value
