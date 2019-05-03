from toga_wpf.libs import WPF, Controls, System

from .base import Widget


class Box(Widget):

    def create(self) -> None:
        self.native = Controls.Canvas()
        # self.native.HorizontalAlignment = WPF.HorizontalAlignment.Stretch
        # self.native.VerticalAlignment = WPF.VerticalAlignment.Stretch
        # self.native.Width = System.Double.NaN
        # self.native.Height = System.Double.NaN

    def add_child(self, child: Widget) -> None:
        self.native.Children.Add(child.native)
