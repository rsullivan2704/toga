import types
from toga_wpf import WPF
from .base import Widget


class Button(Widget):
    def create(self) -> None:
        self.native = WPF.Controls.Button()

    def set_label(self, label: object) -> None:
        self.native.Content = label

    def set_on_press(self, handler: types.FunctionType) -> None:
        self.native.Click += handler
