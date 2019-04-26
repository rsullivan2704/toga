import sys
import types
from typing import Iterable

import toga

from .libs import WPF, Threading, add_handler
from .window import Window


class MainWindow(Window):
    def on_close(self):
        pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface: toga.App) -> None:
        self.interface = interface
        self.interface._impl = self

    def _create_app_commands(self) -> None:
        self.interface.commands.add(
            toga.Command(None, 'About {name}'.format(name=self.interface.name), group=toga.Group.HELP), # noqa: E501
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Command(lambda s: self.exit(), 'Exit {name}'.format(name=self.interface.name), shortcut='q', group=toga.Group.FILE, section=sys.maxsize), # noqa: E501
            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )

    def create_menus(self) -> None:
        toga.Group.FILE.order = 0
        factory = toga.platform.get_platform_factory()
        # Only create the menu if the menu item index has been created
        # if hasattr(self, '_menu_items'):
        self.menubar = WPF.Controls.Menu()
        group_menu = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK or cmd == toga.SECTION_BREAK:
                self.menubar.Items.Add(WPF.Controls.Separator())
            else:
                group_menus = [menu for menu in self.menubar.Items if hasattr(menu, 'Header') and menu.Header == cmd.group.label] # noqa: E501
                if len(group_menus) > 0:
                    group_menu = group_menus[0]
                else:
                    group_menu = WPF.Controls.MenuItem()
                    group_menu.Header = cmd.group.label
                menu_item = WPF.Controls.MenuItem()
                bound_command = cmd.bind(factory)
                menu_item.Command = bound_command.native
                menu_item.Header = cmd.label
                cmd._widgets.append(menu_item)
                group_menu.Items.Add(menu_item)
            if group_menu not in self.menubar.Items:
                self.menubar.Items.Add(group_menu)

    def create(self) -> None:
        self.native = WPF.Application()
        self._create_app_commands()

        # Call user code to populate the main window
        self.create_menus()
        self.interface.startup()
        # self.interface.main_window._impl.native.Icon = self.interface.icon.bind(self.interface.factory).native  # noqa: E501

    def run_app(self) -> None:
        self.create()
        self.native.Run(self.interface.main_window._impl.native)

    def set_on_exit(self, handler: types.FunctionType) -> None:
        try:
            self.native.Exit += add_handler(handler)
        except AttributeError:
            pass

    def current_window(self) -> None:
        self.interface.factor.not_implemented('App.current_window()')

    def enter_full_screen(self, windows: Iterable[toga.Window]) -> None:
        for window in windows:
            window._impl.native.WindowState = WPF.WindowState.Maximized
            window._impl.native.WindowStyle = 0  # WPF.WindowStyle.None ".None" throws a syntax error  # noqa: E501

    def exit_full_screen(self, windows: Iterable[toga.Window]) -> None:
        for window in windows:
            window._impl.native.WindowState = WPF.WindowState.Normal
            window._impl.native.WindowStyle = WPF.WindowStyle.SingleBorderWindow  # noqa: E501

    def show_cursor(self) -> None:
        pass

    def hide_cursor(self) -> None:
        pass

    def main_loop(self) -> None:
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))  # noqa: E501
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def exit(self) -> None:
        self.native.Exit()
