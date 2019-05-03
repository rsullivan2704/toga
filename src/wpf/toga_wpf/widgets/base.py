from typing import Union

from travertino.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP
from travertino.size import at_least

import toga
from toga_wpf import colors, factory
from toga_wpf.libs import WPF, Controls, ArgumentException, Enum, System, __logger__


class Widget:
    def __init__(self, interface: toga.Widget) -> None:
        self.interface = interface
        self.interface._impl = self

        self.native = None
        self.create()
        self.native.IsEnabled = interface.enabled
        self.native.LayoutUpdated += self._layout_updated_handler
        # self.native.SizeChanged += self._size_changed_handler
        # self.native.Loaded += self._loaded_handler
        self.interface.style.reapply()

    def _layout_updated_handler(self, sender: System.Object, args: WPF.RoutedEventArgs) -> None:
        self.rehint()
        self.interface.style.reapply()

    def rehint(self) -> None:
        self.interface.intrinsic.width = self.native.DesiredSize.Width
        self.interface.intrinsic.height = self.native.DesiredSize.Height

    def add_child(self, child: 'Widget') -> None:
        pass

    def set_app(self, app: toga.App) -> None:
        pass

    def set_window(self, window: toga.Window) -> None:
        pass

    def set_enabled(self, value: bool) -> None:
        try:
            self.native.IsEnabled = value
        except AttributeError as ex:
            __logger__.info('AttributeError in set_enabled method call\n{exception}'.format(exception=str(ex)))
            pass

# region Applicator Methods

    def vertical_shift(self) -> None:
        return 0

    def set_bounds(self, x: int, y: int, width: int, height: int) -> None:
        try:
            # Root level widgets may require vertical adjustment to
            # account for toolbars, etc
            # if self.interface.parent is not None:
            #     vertical_shift = self.frame.vertical_shift
            # else:
            #     vertical_shift = 0

            # only set the top and left positions if
            # this is not the root dock panel.
            if self.interface.parent is not None:
                Controls.Canvas.SetTop(self.native, x)
                Controls.Canvas.SetLeft(self.native, y)

            self.native.Width = width
            self.native.Height = height
        except AttributeError as ae:
            __logger__.info('Error in set_bounds method call:\n{message}'.format(message=str(ae)))  # noqa: E501
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
            except (AttributeError, ArgumentException) as ex:
                __logger__.info('Error in set_alignment method call:\n{message}'.format(message=str(ex)))

    def set_hidden(self, hidden: bool) -> None:
        try:
            if hidden:
                visibility = WPF.Visibility.Hidden
            else:
                visibility = WPF.Visibility.Visible
            self.native.Visibility = visibility
        except AttributeError as ex:
            __logger__.info('Error in set_alignment method call:\n{message}'.format(message=str(ex)))
            pass

    def set_font(self, font: toga.Font) -> None:
        font.bind(factory)
        self.native.FontFamily = font._impl.native.typeface.FontFamily
        self.native.FontSize = font._impl.native.size
        self.native.FontStyle = font._impl.native.typeface.Style
        self.native.FontWeight = font._impl.native.typeface.Weight

    def set_color(self, color: toga.colors.Color) -> None:
        if color:
            try:
                self.native.Foreground = colors.get_brush(color)
            except (AttributeError, ArgumentException) as ex:
                __logger__.error(str(ex))
                raise

    def set_background_color(self, color: toga.colors.Color) -> None:
        if color:
            try:
                self.native.Background = colors.get_brush(color)
            except (AttributeError, ArgumentException) as ex:
                __logger__.error(str(ex))
                raise

# endregion
