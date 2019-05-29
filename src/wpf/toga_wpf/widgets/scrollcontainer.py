import toga

from toga_wpf.viewport import WPFViewport
from toga_wpf.widgets.base import Widget

from toga_wpf.libs import Controls, WPF, __logger__


class ScrollContainer(Widget):

    def create(self) -> None:
        self.native = Controls.ScrollViewer()
        self.native.Content = Controls.Grid()
        self.native.SizeChanged += self.container_size_changed_handler

    def set_content(self, widget: Widget) -> None:
        self.native.Content.Children.Clear()
        self.native.Content.Children.Add(widget.native)
        widget.viewport = WPFViewport(self.native, self)
        widget.frame = self

    def set_vertical(self, value: bool) -> None:
        if value:
            self.native.VerticalScrollBarVisibility = Controls.ScrollBarVisibility.Auto  # noqa: E501
        else:
            self.native.VerticalScrollBarVisibility = Controls.ScrollBarVisibility.Hidden  # noqa: E501

    def set_horizontal(self, value: bool) -> None:
        if value:
            self.native.HorizontalScrollBarVisibility = Controls.ScrollBarVisibility.Auto  # noqa: E501
        else:
            self.native.HorizontalScrollbarVisibility = Controls.ScrollBarVisibility.Hidden  # noqa: E501
