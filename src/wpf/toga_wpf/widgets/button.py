import toga

from toga.handlers import wrapped_handler

from toga_wpf.libs import WPF, Controls, __logger__

from toga_wpf.widgets.base import Widget


class WPFButton(Controls.Button):
    def __init__(self, interface: toga.Button) -> None:
        super().__init__()
        self.interface = interface
        self.Click += self.on_click

    def on_click(self, sender: Controls.Button, eventargs: WPF.RoutedEventArgs) -> None:  # noqa: E501
        try:
            self.interface.on_press(self.interface)
        except AttributeError as ex:
            __logger__.info('Passing on AttributeError in WPFButton.on_click\n{message}'.format(message=str(ex)))
            pass
        except TypeError:
            __logger__.info('Button.on_press handler not defined.')
            pass


class Button(Widget):
    def create(self) -> None:
        self.native = WPFButton(self.interface)

    def set_label(self, label: object) -> None:
        self.native.Content = label

    def set_on_press(self, handler: type(wrapped_handler)) -> None:  # noqa: E501
        __logger__.debug('Passing toga_wpf.Button.set_on_press')
        pass
