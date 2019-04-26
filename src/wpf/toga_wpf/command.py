import toga

from .libs import System, Input


class DelegateCommand(Input.ICommand):
    __namespace__ = 'toga_wpf'

    def __init__(self) -> None:
        self.can_execute_changed_handlers = []

    def add_CanExecuteChanged(self, handler):
        self.can_execute_changed_handlers.append(handler)

    def remove_CanExecuteChanged(self, handler):
        self.can_execute_changed_handlers.remove(handler)

    def Execute(self, parameter) -> None:
        self._execute(parameter)

    def set_Execute(self, action) -> None:
        self._execute = action

    def CanExecute(self, parameter) -> bool:
        return True if self._can_execute is None else self._can_execute(parameter)  # noqa: E501

    def set_CanExecute(self, predicate) -> None:
        self._can_execute = predicate

    def OnCanExecuteChanged(self) -> None:
        for handler in self.can_execute_changed_handlers:
            handler(self, System.EventArgs.Empty)


class Command:
    def __init__(self, interface: toga.Command) -> None:
        self.interface = interface
        self.native = None
        if self.interface.action is not None:
            # action_delegate = System.Action(self.action)
            self.native = DelegateCommand()
            self.native.set_Execute(self.action)
            self.native.set_CanExecute(self.predicate)

    def action(self, parameter) -> None:
        self.interface.action(parameter)

    def predicate(self, parameter) -> bool:
        return self.interface.enabled
