import toga

from toga_wpf.viewport import WPFViewport

from toga_wpf.libs import Controls, WPF, __logger__

from toga_wpf.widgets.base import Widget


class WPFTabControlViewport(WPFViewport):
    @property
    def height(self) -> float:
        try:
            return self.native.ActualHeight - self.native.SelectedItem.ActualHeight - self.native.SelectedItem.Padding.Top - self.native.SelectedItem.Padding.Bottom
        except AttributeError:
            return self.native.ActualHeight

    @property
    def width(self) -> float:
        try:
            return self.native.ActualWidth - self.native.SelectedItem.Padding.Left - self.native.SelectedItem.Padding.Right
        except AttributeError:
            return self.native.ActualWidth


class WPFTabControl(Controls.TabControl):
    def __init__(self, interface: toga.OptionContainer) -> None:
        super().__init__()
        self.interface = interface
        self.SelectionChanged += self.on_selection_changed

    def on_selection_changed(self, sender: Controls.TabControl, eventargs: Controls.SelectionChangedEventArgs) -> None:
        try:
            self.interface.on_select()
        except AttributeError:
            __logger__.info('Passing AttributeError in WPFTabControl.on_selection_changed')
            pass
        except TypeError:
            __logger__.info('OptionContainer.on_select handler not defined.')
            pass


class OptionContainer(Widget):
    def create(self) -> None:
        self.native = WPFTabControl(self.interface)
        self.native.SizeChanged += self.container_size_changed_handler

    def add_content(self, label: str, widget: Widget) -> None:
        widget.viewport = WPFTabControlViewport(self.native, self)
        widget.frame = self
        tab = Controls.TabItem()
        tab.Header = label
        tab.Content = widget.native
        self.native.Items.Add(tab)

    def set_on_select(self, handler):
        __logger__.debug('Passing toga_wpf.OptionContainer.set_on_select.')
        pass

    def container_size_changed_handler(self, sender: WPF.FrameworkElement, event: WPF.SizeChangedEventArgs) -> None:
        try:
            for tab in self.interface.content:
                tab.refresh()
            # self.interface.content.refresh()
        except AttributeError:
            __logger__.info('Passing AttributeError in OptionContainer.container_size_changed_handler.')
            pass
