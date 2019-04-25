import toga

from .libs import System, Input


class DelegateCommand(Input.ICommand):
    # TODO: Have to figure this out
    __namespace__ = 'toga_wpf'

    def __init__(self) -> None:
        self.CanExecuteChanged += self._can_execute_changed

    def _can_execute_changed(sender, args) -> None:
        pass

    def CanExecute(self, parameter: System.Object) -> bool:
        return True if self._can_execute is None else self._can_execute(parameter)  # noqa: E501

    def set_canexecute(self, predicate: System.Predicate[System.Object]) -> None:  # noqa: E501
        self._can_execute = predicate

    def Execute(self, parameter: System.Object) -> None:
        try:
            self._execute(parameter)
        except AttributeError:
            pass

    def set_execute(self, action: System.Action[System.Object]) -> None:
        self._execute = action


class Command:
    def __init__(self, interface: toga.Command) -> None:
        self.interface = interface
        self.native = None
        if self.interface.action is not None:
            def can_execute(interface: toga.Command) -> bool:
                return interface.enabled
            action = System.Action(self.interface.action)
            predicate = System.Predicate[System.Object](can_execute)
            self.native = DelegateCommand()
            self.native.set_canexecute(predicate)
            self.native.set_execute(action)
