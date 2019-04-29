import builtins
from typing import Union

from travertino.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP

import toga
from toga_wpf import colors, factory
from toga_wpf.libs import WPF, ArgumentException, Enum, FontFamily


class Widget:
    def __init__(self, interface: toga.Widget) -> None:
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def rehint(self) -> None:
        pass

    def add_child(self, child: 'Widget') -> None:
        pass

    def set_app(self, app: toga.App) -> None:
        pass

    def set_window(self, window: toga.Window) -> None:
        pass

    def set_enabled(self, value: bool) -> None:
        try:
            self.native.IsEnabled = value
        except AttributeError:
            pass

# region Applicator Methods

    def vertical_shift(self) -> None:
        return 0

    def set_bounds(self, x: int, y: int, width: int, height: int) -> None:
        if self.native:
            # Root level widgets may require vertical adjustment to
            # account for toolbars, etc
            if self.interface.parent is None:
                vertical_shift = self.frame.vertical_shift
            else:
                vertical_shift = 0

            self.native.Width = width
            self.native.Height = height
            try:
                self.native.Left = x
                self.native.Top = y + vertical_shift
            except AttributeError:
                pass

    def set_alignment(self, alignment: Union[LEFT, RIGHT, TOP, BOTTOM, CENTER, JUSTIFY]) -> None:  # noqa: E501
        if alignment == JUSTIFY:
            alignment = 'Stretch'
        # FIXME Have to figure out how to determine when
        # Stretch (JUSTIFY) applies to Horizontal vs Vertical.
        # For now Horizontal takes precedence.
        try:
            align = Enum.Parse(WPF.HorizontalAlignment, alignment, True)
            self.native.HorizontalAlignment = align
        except (AttributeError, ArgumentException):
            # ArgumentException means we tried to set
            # horizontal alignment with a vertical alignment value
            try:
                align = Enum.Parse(WPF.VerticalAlignment, alignment, True)
                self.native.VerticalAlignment = align
            except (AttributeError, ArgumentException):
                # The above calls will always fail since we cannot get the
                # actual enum Type from pythonnet.
                # TODO: Have to figure out how to parse a .net Enum from
                # a text value, ignoring case
                factory.not_implemented('Applicator.text_alignment')

    def set_hidden(self, hidden: bool) -> None:
        try:
            if hidden:
                visibility = WPF.Visibility.Hidden
            else:
                visibility = WPF.Visibility.Visible
            self.native.Visibility = visibility
        except AttributeError:
            pass

    def set_font(self, font: toga.Font) -> None:
        font.bind(factory)
        self.native.FontFamily = font._impl.native.typeface.FontFamily
        self.native.FontSize = font._impl.native.size
        self.native.FontStyle = font._impl.native.typeface.Style
        self.native.FontWeight = font._impl.native.typeface.Weight

    def set_color(self, color: toga.colors.Color) -> None:
        try:
            self.native.Foreground = colors.get_brush(color)
        except (AttributeError, ArgumentException):
            pass

    def set_background_color(self, color: toga.colors.Color) -> None:
        try:
            self.native.Background = colors.get_brush(color)
        except (AttributeError, ArgumentException):
            pass

# endregion
