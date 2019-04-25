from toga_wpf.libs import WPF

from .base import Widget


class Box(Widget):

    def create(self) -> None:
        self.native = WPF.Controls.StackPanel()

    def add_child(self, child: Widget) -> None:
        self.native.Children.Add(child.native)
