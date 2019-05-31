import toga
from toga.handlers import wrapped_handler

from toga_wpf.widgets.base import Widget
from toga_wpf.libs import Controls, __logger__


class WPFTextBox(Controls.TextBox):
    def __init__(self, interface: toga.TextInput) -> None:
        super().__init__()
        self.interface = interface
        self.TextChanged += self.on_text_changed

    def on_text_changed(self, sender: Controls.TextBox, eventargs: Controls.TextChangedEventArgs) -> None:
        try:
            self.interface.on_change(self.interface)
        except AttributeError as ex:
            __logger__.info('Passing on AttributeError in WPFTextBox.on_change\n{message}'.format(message=str(ex)))
            pass
        except TypeError:
            __logger__.info('TextInput.on_change handler not defined.')
            pass


class TextInput(Widget):
    def create(self) -> None:
        self.native = WPFTextBox(self.interface)

    def set_readonly(self, value: bool) -> None:
        self.native.IsReadOnly = value

    def set_placeholder(self, value: str) -> None:
        self.interface.factory.not_implemented('TextInput.set_placeholder')

    def get_value(self) -> str:
        return self.native.Text

    def set_value(self, value: str) -> None:
        self.native.Text = value

    def set_on_change(self, handler: wrapped_handler) -> None:
        __logger__.debug('Passing TextInput.set_on_change')
        pass
