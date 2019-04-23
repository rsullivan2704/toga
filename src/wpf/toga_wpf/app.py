import sys
import toga
from .libs import Threading, WPF
from .window import Window
from typing import Iterable


class MainWindow(Window):
    def on_close(self):
        pass


class App:
    T = TypeVar('T', toga.Window)
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface: toga.App) -> None:
        self.interface = interface
        self.interface._impl = self

    def create(self) -> None:
        self.native = WPF.Application()
        self._create_app_commands()

        # Call user code to populate the main window
        self.interface.startup()
        self.create_menus()
        self.interface.main_window._impl.native.Icon = self.interface.icon.bind(self.interface.factory).native  # noqa: E501

    def _create_app_commands(self) -> None:
        self.interface.commands.add(
            toga.Command(None, f'About {self.interface.name}', group=toga.Group.HELP) # noqa: E501
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Comand(lambda s: self.exit(), f'Exit {self.interface.name}', shortcut='q', group=toga.Group.FILE, section=sys.maxsize), # noqa: E501
            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )

    def create_menus(self) -> None:
        toga.Group.FILE.order = 0
        # Only create the menu if the menu item index has been created
        # if hasattr(self, '_menu_items'):
        menubar = WPF.Controls.Menu()
        group_menu = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK:
                menubar.Items.Add(WPF.Controls.Separator())
            elif cmd == toga.SECTION_BREAK:
                menubar.Items.Add(WPF.Controls.Separator())
            else:
                try:
                    group_menu = [menu for menu in menubar.Items if menu.Header == cmd.group.label][0] # noqa: E501
                except IndexError as exc:
                    group_menu = WPF.Controls.MenuItem()
                    group_menu.Header = cmd.group.label
                except Exception as ex:
                    raise
                menu_item = WPF.Controls.MenuItem()
                menu_item.Command = cmd
                cmd._widgets.append(menu_item)
                group_menu.Items.Add(menu_item)
        menubar.Items.Add(group_menu)
        self.interface.main_window._impl.native.Controls.Add(menubar)
        self.interface.main_window._impl.native.MainMenuStrip = menubar
        self.interface.main_window.content.refresh()

    def run_app(self) -> None:
        self.create()
        self.native.Run(self.interface.main_window._impl.native)

    def main_loop(self) -> None:
        thread: Threading.Thread = Threading.Thread(Threading.ThreadStart(self.run_app))  # noqa: E501
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def exit(self) -> None:
        self.native.Exit()

    def set_on_exit(self) -> None:
        pass

    def current_window(self) -> None:
        self.interface.factor.not_implemented('App.current_window()')

    def set_full_screen(self, windows: Iterable[Window]) -> None:
        
