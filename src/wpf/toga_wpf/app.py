import sys
from typing import Iterable

import toga
from toga.handlers import wrapped_handler

from .libs import Controls, WPF, Threading, add_handler, __logger__
from .window import Window


class MainWindow(Window):
    def on_close(self):
        __logger__.debug('Passing MainWindow.on_close method call.')
        pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface: toga.App) -> None:
        self.interface = interface
        self.interface._impl = self

    def create(self) -> None:
        self.native = WPF.Application()
        self.create_app_commands()

        # Call user code to populate the main window
        self.create_menus()
        self.interface.startup()
        # self.interface.main_window._impl.native.Icon = self.interface.icon.bind(self.interface.factory).native  # noqa: E501

    def create_menus(self) -> None:
        toga.Group.FILE.order = 0
        factory = toga.platform.get_platform_factory()
        # Only create the menu if the menu item index has been created
        # if hasattr(self, '_menu_items'):
        self.menubar = Controls.Menu()
        # self.menubar.HorizontalAlignment = WPF.HorizontalAlignment.Left
        group_menu = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK or cmd == toga.SECTION_BREAK:
                self.menubar.Items.Add(Controls.Separator())
            else:
                group_menus = [menu for menu in self.menubar.Items if hasattr(menu, 'Header') and menu.Header == cmd.group.label] # noqa: E501
                if len(group_menus) > 0:
                    group_menu = group_menus[0]
                else:
                    group_menu = Controls.MenuItem()
                    group_menu.Header = cmd.group.label
                menu_item = Controls.MenuItem()
                bound_command = cmd.bind(factory)
                menu_item.Command = bound_command.native
                menu_item.Header = cmd.label
                cmd._widgets.append(menu_item)
                group_menu.Items.Add(menu_item)
            if group_menu not in self.menubar.Items:
                self.menubar.Items.Add(group_menu)

    def main_loop(self) -> None:
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))  # noqa: E501
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def exit(self) -> None:
        return WPF.Application.Current.Shutdown()

    def set_on_exit(self, handler: wrapped_handler) -> None:
        try:
            self.native.Exit += add_handler(handler)
        except AttributeError:
            __logger__.info('Passing AttributeError in App.set_on_exit method call.')
            pass

    def current_window(self) -> None:
        return WPF.Application.Current.Windows.OfType[WPF.Window]().FirstOrDefault(lambda x: x.IsActive)  # noqa: E501

    def enter_full_screen(self, windows: Iterable[toga.Window]) -> None:
        for window in windows:
            window.full_screen = True

    def exit_full_screen(self, windows: Iterable[toga.Window]) -> None:
        for window in windows:
            window.full_screen = False

    def show_cursor(self) -> None:
        __logger__.debug('Passing App.show_cursor method call.')
        pass

    def hide_cursor(self) -> None:
        __logger__.debug('Passing App.hide_cursor method call.')
        pass

    def create_app_commands(self) -> None:
        self.interface.commands.add(
            toga.Command(None, 'About {name}'.format(name=self.interface.name), group=toga.Group.HELP), # noqa: E501
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Command(lambda s: self.exit(), 'Exit {name}'.format(name=self.interface.name), shortcut='q', group=toga.Group.FILE, section=sys.maxsize), # noqa: E501
            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )

    def run_app(self) -> None:
        self.create()
        self.native.Run(self.interface.main_window._impl.native)
