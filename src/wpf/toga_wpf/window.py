from travertino.layout import Viewport

import toga
from toga import GROUP_BREAK, SECTION_BREAK

from .libs import WPF, System, add_handler
from .widgets import base


class WinWPFViewport:
    def __init__(self, native: WPF.Window, frame: toga.Window) -> None:  # FIXME need to find the type for frame # noqa: E501
        self.native = native
        self.frame = frame
        self.dpi = 96

    @property
    def width(self) -> float:
        return self.native.ActualWidth

    @property
    def height(self) -> float:
        return self.native.ActualHeight - self.frame.vertical_shift


class Window:
    def __init__(self, interface: toga.Window) -> None:
        self.interface = interface
        self.interface._impl = self
        self.create()

    def _on_size_changed(self, sender, event) -> None:  # noqa: E501
        try:
            # re-layout the content
            self.interface.content.refresh()
        except AttributeError:
            pass

    def create(self) -> None:
        self.native = WPF.Window()
        self.native.Width = self.interface._size[0]
        self.native.Height = self.interface._size[1]
        self.native.interface = self.interface
        self.native.SizeChanged += self._on_size_changed
        self.toolbar_native = None  # type: WPF.Controls.ToolBarTray
        self.toolbar_items = None  # type: WPF.Controls.Button

    def create_toolbar(self) -> None:
        tb = WPF.Controls.ToolBar()
        self.toolbar_native = WPF.Controls.ToolBarTray()
        self.toolbar_native.ToolBars.Add(tb) # noqa: E501
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK or cmd == SECTION_BREAK:
                item = WPF.Controls.Separator()
            else:
                cmd.bind(self.interface.factory)
                item = WPF.Controls.Button()
                item.Command = cmd.native
            tb.Items.add(item)
        self.native.Content.Children.Add(self.toolbar_native)

    def set_app(self, app: toga.App) -> None:
        pass

    @property
    def vertical_shift(self) -> int:
        result = 0
        try:
            result += self.native.interface._impl.toolbar_native.ActualHeight
        except AttributeError:
            pass
        try:
            result += self.native.interface._impl.native.MainMenuStrip.Height
        except AttributeError:
            pass
        return result

    def set_title(self, title: str) -> None:
        self.native.Title = title

    def set_content(self, widget: base.Widget) -> None:
        self.native.Content = WPF.Controls.DockPanel()
        if self.toolbar_native:
            self.native.Content.Children.Add(self.toolbar_native)
        widget.viewport = WinWPFViewport(self.native, self)
        widget.frame = self
        self.native.Content.Children.Add(widget.native)

    def set_position(self, position: tuple) -> None:
        pass

    def set_size(self, size: tuple) -> None:
        pass

    def show(self) -> None:
        self.native.Show()
