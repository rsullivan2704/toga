import toga

from .libs import System, Input


class DelegateCommand(Input.ICommand):
    def __init__(self, execute: Input.Action[object], can_execute: System.Predicate[object] = None) -> None:  # noqa: E501
        self._execute = execute
        self._can_execute = can_execute

    def can_execute(self, parameter: object) -> bool:
        if self._can_execute is None:
            return True
        return self._can_execute(parameter)

    def execute(self, parameter: object) -> None:
        self._execute(parameter)


class Command:
    def __init__(self, interface: toga.Command) -> None:
        self.interface = interface
