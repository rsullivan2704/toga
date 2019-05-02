from toga_wpf.libs import Controls

from .base import Widget


class Box(Widget):

    def create(self) -> None:
        self.native = Controls.Canvas()

    def add_child(self, child: Widget) -> None:
        self.native.Children.Add(child.native)
