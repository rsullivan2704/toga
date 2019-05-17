from typing import Union

from toga.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP

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
        # self.native.LayoutUpdated += self._layout_updated_handler
        self.rehint_count = 0
        # self.native.SizeChanged += self._size_changed_handler
        # self.native.Loaded += self._loaded_handler
        # self.interface.style.reapply()

    def set_app(self, app: toga.App) -> None:
        pass

    def set_window(self, window: toga.Window) -> None:
        pass

    @property
    def container(self) -> None:
        pass

    @container.setter
    def container(self, container: object) -> None:
        pass

    def set_enabled(self, value: bool) -> None:
        # pass
        try:
            self.native.IsEnabled = value
        except AttributeError as ex:
            __logger__.info('AttributeError in set_enabled method call\n{exception}'.format(exception=str(ex)))
            pass

# region Applicator

    def set_bounds(self, x: int, y: int, width: int, height: int) -> None:
        pass
        # try:
        #     # only set the bounds if
        #     # this is not the root widget.
        #     if self.interface.parent is not None:
        #         Controls.Canvas.SetTop(self.native, x)
        #         Controls.Canvas.SetLeft(self.native, y)
        #         self.native.Width = width
        #         self.native.Height = height
        # except AttributeError as ae:
        #     __logger__.info('Passing on AttributeError in Widget.set_bounds method call:\n{message}'.format(message=str(ae)))  # noqa: E501
        #     pass

    def set_hidden(self, hidden: bool) -> None:
        pass
        # try:
        #     if hidden:
        #         visibility = WPF.Visibility.Hidden
        #     else:
        #         visibility = WPF.Visibility.Visible
        #     self.native.Visibility = visibility
        # except AttributeError as ex:
        #     __logger__.info('Error in set_alignment method call:\n{message}'.format(message=str(ex)))
        #     pass

    def set_font(self, font: toga.Font) -> None:
        pass
        # font.bind(factory)
        # self.native.FontFamily = font._impl.native.typeface.FontFamily
        # self.native.FontSize = font._impl.native.size
        # self.native.FontStyle = font._impl.native.typeface.Style
        # self.native.FontWeight = font._impl.native.typeface.Weight

    def set_background_color(self, color: toga.colors.Color) -> None:
        # pass
        if color:
            try:
                self.native.Background = colors.native_color(color)
            except (AttributeError, ArgumentException) as ex:
                __logger__.error(str(ex))
                raise

    def set_alignment(self, alignment: Union[LEFT, RIGHT, TOP, BOTTOM, CENTER, JUSTIFY]) -> None:  # noqa: E501
        pass
        # if alignment == JUSTIFY:
        #     alignment = 'Stretch'
        # # FIXME Have to figure out how to determine when
        # # Stretch (JUSTIFY) applies to Horizontal vs Vertical.
        # # For now Horizontal takes precedence.
        # try:
        #     align = Enum.Parse(WPF.HorizontalAlignment, alignment, True)
        #     self.native.HorizontalAlignment = align
        # except (AttributeError, ArgumentException):
        #     # ArgumentException means we tried to set
        #     # horizontal alignment with a vertical alignment value
        #     try:
        #         align = Enum.Parse(WPF.VerticalAlignment, alignment, True)
        #         self.native.VerticalAlignment = align
        #     except (AttributeError, ArgumentException) as ex:
        #         __logger__.info('Error in set_alignment method call:\n{message}'.format(message=str(ex)))

    def set_color(self, color: toga.colors.Color) -> None:
        pass
        # if color:
        #     try:
        #         self.native.Foreground = colors.native_color(color)
        #     except (AttributeError, ArgumentException) as ex:
        #         __logger__.error(str(ex))
        #         raise

    def vertical_shift(self) -> None:
        return 0

# endregion

    def add_child(self, child: 'Widget') -> None:
        pass

    def rehint(self) -> None:
        self.rehint_count += 1
        debug_msg = \
            '''
            object = {obj}
            rehint count = {rehint_count}
            intrinsic width = {intr_width}
            intrinsic height = {intr_height}
            native width = {native_width}
            native height = {native_height}
            '''.format(
                obj=self,
                rehint_count=self.rehint_count,
                intr_width=self.interface.intrinsic.width,
                intr_height=self.interface.intrinsic.height,
                native_width=self.native.ActualWidth,
                native_height=self.native.ActualHeight,
            )
        __logger__.debug(debug_msg)
        self.interface.intrinsic.width = self.native.ActualWidth
        self.interface.intrinsic.height = self.native.ActualHeight

    # def _size_changed_handler(self, sender: System.Object, args: WPF.RoutedEventArgs) -> None:
    #     self.rehint()
        # self.interface.style.reapply()
