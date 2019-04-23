import toga

from .libs import WPF


class Command:

    def native_action(self, sender, event) -> None:
        try:
            self.interface.action(sender, event)
        except AttributeError:
            pass

    def native_enabled(self, sender, event) -> None:
        try:
            event.CanExecute = self.interface.enabled
        except AttributeError:
            pass

    def __init__(self, interface: toga.Command) -> None:
        self.interface = interface
        self.native_command = WPF.Input.RoutedUICommand()
        self.native_command.Text = interface.label
        native_action = WPF.Input.ExecutedRoutedEventHandler()
        self.native = WPF.Input.CommandBinding(self.native_command, native_action, native_enabled)  # noqa: E501
