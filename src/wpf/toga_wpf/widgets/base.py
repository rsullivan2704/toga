from typing import Union

from toga.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP

import toga
from toga_wpf import colors, factory
from toga_wpf.libs import WPF, System, Controls, ArgumentException, Enum, __logger__


class Widget:
    def __init__(self, interface: toga.Widget) -> None:
        self.interface = interface
        self.interface._impl = self

        self.native = None
        # Create the native
        self.create()
        self.native.interface = interface
        self.rehint_count = 0
        self.interface.style.reapply()

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
            __logger__.info('AttributeError in Widget.set_enabled\n{exception}'.format(exception=str(ex)))
            pass

# region Applicator

    def set_bounds(self, x: int, y: int, width: int, height: int) -> None:
        # pass
        try:
            debug_msg = \
                '''
                Widget.set_bounds(x, y, width, height):
                object = {obj}
                x pos = {x_pos}, adjusted x = {adjusted_x}
                y pos = {y_pos}, adjusted y = {adjusted_y}
                width  = {width},  native width  = {native_width}
                height = {height}, native height = {native_height}
                parent = {parent}, parent layout = {parent_layout}
                '''
            adj_pos = self.get_adjusted_position(self.interface, x, y)
            # only set the position if
            # this is not the root widget.
            if self.interface.parent is not None:
                debug_msg = debug_msg.format(
                    obj=self,
                    x_pos=x,
                    adjusted_x=adj_pos[0],
                    y_pos=y,
                    adjusted_y=adj_pos[1],
                    width=width,
                    native_width=self.native.ActualWidth,
                    height=height,
                    native_height=self.native.ActualHeight,
                    parent=self.interface.parent,
                    parent_layout=self.interface.parent.layout
                )
                __logger__.debug(debug_msg)
                Controls.Canvas.SetLeft(self.native, adj_pos[0])
                Controls.Canvas.SetTop(self.native, adj_pos[1])
            else:
                debug_msg = debug_msg.format(
                    obj=self,
                    x_pos=x,
                    adjusted_x=adj_pos[0],
                    y_pos=y,
                    adjusted_y=adj_pos[1],
                    width=width,
                    native_width=self.native.ActualWidth,
                    height=height,
                    native_height=self.native.ActualHeight,
                    parent=None,
                    parent_layout=None
                )
                __logger__.debug(debug_msg)
            self.native.Width = width
            self.native.Height = height
        except AttributeError as ae:
            __logger__.info('Passing AttributeError in Widget.set_bounds:\n{message}'.format(message=str(ae)))  # noqa: E501
            pass

    def set_hidden(self, hidden: bool) -> None:
        # pass
        try:
            if hidden:
                visibility = WPF.Visibility.Hidden
            else:
                visibility = WPF.Visibility.Visible
            self.native.Visibility = visibility
        except AttributeError as ex:
            __logger__.info('Passing AttributeError in Widget.set_hidden:\n{message}'.format(message=str(ex)))
            pass

    def set_font(self, font: toga.Font) -> None:
        # pass
        font.bind(factory)
        self.native.FontFamily = font._impl.native.typeface.FontFamily
        self.native.FontSize = font._impl.native.size
        self.native.FontStyle = font._impl.native.typeface.Style
        self.native.FontWeight = font._impl.native.typeface.Weight

    def set_background_color(self, color: toga.colors.Color) -> None:
        # pass
        if color:
            try:
                self.native.Background = colors.native_color(color)
            except (Exception) as ex:
                __logger__.error(str(ex))
                raise

    def set_alignment(self, alignment: Union[LEFT, RIGHT, TOP, BOTTOM, CENTER, JUSTIFY]) -> None:  # noqa: E501
        # pass
        if alignment == JUSTIFY:
            alignment = 'Stretch'
        # FIXME Have to figure out how to determine when
        # Stretch (JUSTIFY) applies to Horizontal vs Vertical.
        # For now Horizontal takes precedence.
        try:
            align = Enum.Parse(WPF.HorizontalAlignment, alignment, True)
            self.native.HorizontalContentAlignment = align
        except ArgumentException as hor_argexc:
            # ArgumentException means we tried to set
            # horizontal alignment with a vertical alignment value
            __logger__.debug('HorizontalAlignment Enum.Parse failed. Attempting VerticalAlignment Enum.Parse.\n{message}'.format(message=str(hor_argexc)))
            try:
                align = Enum.Parse(WPF.VerticalAlignment, alignment, True)
                self.native.VerticalContentAlignment = align
            except ArgumentException as vert_argexc:
                __logger__.debug('VerticalAlignment Enum.Parse failed:\n{message}'.format(message=str(vert_argexc)))
        except Exception as ex:
            __logger__.info('Failed to set alignment:\n{message}'.format(message=str(ex)))

    def set_color(self, color: toga.colors.Color) -> None:
        # pass
        if color:
            try:
                self.native.Foreground = colors.native_color(color)
            except (AttributeError, ArgumentException) as ex:
                __logger__.error(str(ex))
                raise

    def vertical_shift(self) -> None:
        return 0

# endregion

    def add_child(self, child: 'Widget') -> None:
        pass

    def rehint(self) -> None:
        self.rehint_count += 1
        debug_msg = \
            '''
            Widget.rehint():
            object = {obj}
            rehint count = {rehint_count}
            intrinsic width  = {intr_width},  native width  = {native_width}
            intrinsic height = {intr_height}, native height = {native_height}
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

    def container_size_changed_handler(self, sender: WPF.FrameworkElement, event: WPF.SizeChangedEventArgs) -> None:
        try:
            self.interface.content.refresh()
        except AttributeError:
            __logger__.info('Passing AttributeError in Widget.container_size_changed_handler.')
            pass

    def get_adjusted_position(self, interface, x, y):
        parent = interface.parent
        if parent is None:
            return (x, y)
        else:
            # TODO: Have to revisit this formula to test for
            # the effect of padding and margin
            adj_x = x - parent.layout.content_left
            adj_y = y - parent.layout.content_top
            return self.get_adjusted_position(parent, adj_x, adj_y)
