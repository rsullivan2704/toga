from travertino.layout import Viewport

import toga
from toga import GROUP_BREAK, SECTION_BREAK

from .libs import Controls, WPF, System, VisualTreeHelper
from .widgets import base


class WinWPFViewport:
    def __init__(self, native: WPF.Window, frame: toga.Window) -> None:
        self.native = native
        self.frame = frame
        self.native.Parent.DpiChanged += self._dpi_changed_handler
        pixels_per_dip = VisualTreeHelper.GetDpi(self.native).PixelsPerDip
        self._dpi = self._calc_dpi(pixels_per_dip)

    def _dpi_changed_handler(self, sender: System.Object, args: WPF.DpiChangedEventArgs) -> None:  # noqa: E501
        self._dpi = self._calc_dpi(args.NewDpi.PixelsPerDip)

    def _calc_dpi(self, pixels_per_dip: float) -> float:
        return pixels_per_dip * 96

    @property
    def dpi(self) -> float:
        return self._dpi

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

    def _size_changed_handler(self, sender, event) -> None:  # noqa: E501
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
        self.native.SizeChanged += self._size_changed_handler
        self.native_toolbar = None  # type: WPF.Controls.ToolBarTray
        self.toolbar_items = None  # type: WPF.Controls.Button

    def create_toolbar(self) -> None:
        tb = Controls.ToolBar()
        self.native_toolbar = Controls.ToolBarTray()
        self.native_toolbar.ToolBars.Add(tb) # noqa: E501
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK or cmd == SECTION_BREAK:
                item = Controls.Separator()
            else:
                cmd.bind(self.interface.factory)
                item = Controls.Button()
                item.Command = cmd.native
            tb.Items.add(item)

    def set_app(self, app: toga.App) -> None:
        pass

    def set_title(self, title: str) -> None:
        self.native.Title = title

    def set_content(self, widget: base.Widget) -> None:
        dock_panel = Controls.DockPanel()
        dock_panel.LastChildFill = False
        try:
            Controls.DockPanel.SetDock(self.interface.app._impl.menubar, Controls.Dock.Top)
            dock_panel.Children.Add(self.interface.app._impl.menubar)
        except System.ArgumentNullException:
            pass
        try:
            dock_panel.Children.Add(self.native_toolbar)
        except System.ArgumentNullException:
            pass
        self.native.Content = dock_panel
        dock_panel.Children.Add(widget.native)
        widget.viewport = WinWPFViewport(dock_panel, self)
        widget.frame = self

    def set_size(self, size: tuple) -> None:
        try:
            self.native.Width = size[0]
            self.native.Height = size[1]
        except AttributeError:
            pass

    def set_position(self, position: tuple) -> None:
        try:
            self.native.Left = position[0]
            self.native.Top = position[1]  # + vertical_shift
        except AttributeError:
            pass

    def show(self) -> None:
        self.native.Show()

    def set_full_screen(self, is_full_screen: bool) -> None:
        if is_full_screen:
            self.native.WindowState = WPF.WindowState.Maximized
            self.native.WindowStyle = 0  # WPF.WindowStyle.None ".None" throws a syntax error  # noqa: E501
        else:
            self.native.WindowState = WPF.WindowState.Normal
            self.native.WindowStyle = WPF.WindowStyle.SingleBorderWindow

    def on_close(self) -> None:
        pass

    @property
    def vertical_shift(self) -> int:
        result = 0
        try:
            result += self.native.interface._impl.native_toolbar.ActualHeight
        except AttributeError:
            pass
        try:
            # TODO: fix this as there is no MainMenuStrip
            result += self.native.interface._impl.native.MainMenuStrip.Height
        except AttributeError:
            pass
        return result
