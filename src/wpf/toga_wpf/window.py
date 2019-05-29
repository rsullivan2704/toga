import toga
from toga import GROUP_BREAK, SECTION_BREAK

from toga_wpf.viewport import WPFViewport
from toga_wpf.libs import Controls, WPF, System, VisualTreeHelper, __logger__
from toga_wpf.widgets import base


class WPFWindowViewport(WPFViewport):
    def __init__(self, native: WPF.Window, frame: 'Window') -> None:
        super().__init__(native, frame)
        self.native.DpiChanged += self._dpi_changed_handler
        pixels_per_dip = VisualTreeHelper.GetDpi(self.native).PixelsPerDip
        self._dpi = self._calc_dpi(pixels_per_dip)

    def _dpi_changed_handler(self, sender: System.Object, args: WPF.DpiChangedEventArgs) -> None:  # noqa: E501
        self._dpi = self._calc_dpi(args.NewDpi.PixelsPerDip)

    def _calc_dpi(self, pixels_per_dip: float) -> float:
        return pixels_per_dip * self.BASE_DPI

    @property
    def height(self) -> float:
        return self.native.Content.ActualHeight - self.frame.vertical_shift


class Window:
    def __init__(self, interface: toga.Window) -> None:
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self) -> None:
        self.native = WPF.Window()
        self.native.SizeChanged += self._size_changed_handler
        self.native.Width = self.interface._size[0]
        self.native.Height = self.interface._size[1]
        self.native.interface = self.interface
        self.native_toolbar = None  # type: WPF.Controls.ToolBarTray
        self.toolbar_items = None  # type: WPF.Controls.Button
        dock_panel = Controls.DockPanel()
        # dock_panel.SizeChanged += self._size_changed_handler
        self.native.Content = dock_panel

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

    def set_content(self, widget: base.Widget) -> None:
        dock_panel = self.native.Content
        dock_panel.Children.Clear()
        try:
            dock_panel.Children.Add(self.interface.app._impl.menubar)
            Controls.DockPanel.SetDock(self.interface.app._impl.menubar, Controls.Dock.Top)
        except System.ArgumentNullException as ex:
            __logger__.error('Menubar cannot be null:\n{exception}'.format(exception=str(ex)))
            raise
        try:
            dock_panel.Children.Add(self.native_toolbar)
            Controls.DockPanel.SetDock(self.native_toolbar, Controls.Dock.Top)
        except System.ArgumentNullException:
            __logger__.info('No toolbar defined.')
            pass
        dock_panel.Children.Add(widget.native)
        widget.viewport = WPFWindowViewport(self.native, self)
        widget.frame = self

    def set_title(self, title: str) -> None:
        self.native.Title = title

    def set_position(self, position: tuple) -> None:
        try:
            self.native.Left = position[0]
            self.native.Top = position[1]  # + vertical_shift
        except AttributeError:
            __logger__.info('passing AttributeError in set_position method.')
            pass

    def set_size(self, size: tuple) -> None:
        try:
            self.native.Width = size[0]
            self.native.Height = size[1]
        except AttributeError:
            __logger__.info('passing AttributeError in set_size method.')
            pass

    def set_app(self, app: toga.App) -> None:
        __logger__.info('Passing Window.set_app method.')
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
        __logger__.info('passing on_close method.')
        pass

    def _size_changed_handler(self, sender: WPF.FrameworkElement, event: WPF.SizeChangedEventArgs) -> None:  # noqa: E501
        try:
            # re-layout the content
            self.interface.content.refresh()
        except AttributeError:
            __logger__.info('Passing AttributeError in Window._size_changed_handler method.')
            pass

    def info_dialog(self, title: str, message: str) -> None:
        pass

    def question_dialog(self, title: str, message: str) -> None:
        pass

    def confirm_dialog(self, title: str, message: str) -> None:
        pass

    def error_dialog(self, title: str, message: str) -> None:
        pass

    def stack_trace_dialog(self, title: str, message: str, content, retry: bool = False) -> None:
        pass

    def save_file_dialog(self, title: str, suggested_filename: str, file_types: str) -> None:
        pass

    @property
    def vertical_shift(self) -> int:
        result = 0
        try:
            result += self.native_toolbar.ActualHeight
        except AttributeError:
            pass
        try:
            result += self.interface.app._impl.menubar.ActualHeight
        except AttributeError:
            pass
        return result
