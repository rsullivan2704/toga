import toga

import typing

from toga.handlers import wrapped_handler

from toga_wpf.libs import WPF

from .base import Widget


class WPFButton(WPF.Controls.Button):
    def __init__(self, interface: toga.Button) -> None:
        super().__init__()
        self.interface = interface
        self.Click += self.on_click

    def on_click(self, sender: WPF.Controls.Button, eventargs: WPF.RoutedEventArgs) -> None:  # noqa: E501
        try:
            self.interface.on_press(self.interface)
        except AttributeError:
            pass


class Button(Widget):
    def create(self) -> None:
        self.native = WPFButton(self.interface)

    def set_label(self, label: object) -> None:
        self.native.Content = label

    def set_on_press(self, handler: type(wrapped_handler)) -> None:  # noqa: E501
        pass
