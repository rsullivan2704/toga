from toga import GROUP_BREAK, SECTION_BREAK
from toga_wpf.widgets import Widget
from travertino.layout import Viewport

from .libs import WPF


class WinWPFViewport:
    def __init__(self, native: WPF.Window, frame: Window) -> None:
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

    def on_size_changed(self, sender: WPF.FrameworkElement, args: WPF.SizeChangedEventArgs) -> None:  # noqa: E501
        if self.interface.content:
            # re-layout the content
            self.interface.content.refresh()

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

    def set_app(self, app: toga.App) -> None:
        # app set when assigning window to the application
        pass

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

    def set_content(self, widget: Widget) -> None:
        pass

    # def set_content(self, widget: toga.Widget) -> None:

