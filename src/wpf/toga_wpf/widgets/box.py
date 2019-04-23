from toga_wpf.libs import WPF

from .base import Widget


class Box(Widget):
    def create(self) -> None:
        self.native = WPF.Controls.StackPanel()
        self.native.interface = self.interface
