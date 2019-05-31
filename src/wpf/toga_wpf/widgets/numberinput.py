from decimal import Decimal

from toga_wpf.widgets.base import Widget
from toga_wpf.libs import WPF, Controls, System, Input, Reflection, FontFamily, __logger__


class NumberInput(Widget):
    def create(self):
        grid = Controls.Grid()
        col_def0 = Controls.ColumnDefinition()
        col_def1 = Controls.ColumnDefinition()
        row_def0 = Controls.RowDefinition()
        row_def1 = Controls.RowDefinition()
        text_box = Controls.TextBox()
        button_up = Controls.Primitives.RepeatButton()
        button_down = Controls.Primitives.RepeatButton()

        grid.Children.Add(text_box)
        grid.Children.Add(button_up)
        grid.Children.Add(button_down)

        self.text_box = text_box
        self.button_down = button_down
        self.button_up = button_up
        self.native = grid

        col_def0.Width = WPF.GridLength(1.0, WPF.GridUnitType.Star)
        col_def1.Width = WPF.GridLength(18.0)
        grid.ColumnDefinitions.Add(col_def0)
        grid.ColumnDefinitions.Add(col_def1)
        row_def0.Height = WPF.GridLength(13.0)
        row_def1.Height = WPF.GridLength(13.0)
        grid.RowDefinitions.Add(row_def0)
        grid.RowDefinitions.Add(row_def1)

        text_box.TextAlignment = WPF.TextAlignment.Right
        text_box.PreviewKeyDown += self.preview_key_down
        text_box.PreviewKeyUp += self.preview_key_up
        text_box.TextChanged += self.text_changed

        # position text_box
        Controls.Grid.SetColumn(text_box, 0)
        Controls.Grid.SetRow(text_box, 0)
        Controls.Grid.SetRowSpan(text_box, 2)

        button_down.VerticalContentAlignment = WPF.VerticalAlignment.Center
        button_down.HorizontalContentAlignment = WPF.HorizontalAlignment.Center
        button_down.FontFamily = FontFamily('Marlett')
        button_down.FontSize = 8.0
        button_down.Content = 6
        button_down.Click += self.button_down_click

        # position button_down
        Controls.Grid.SetColumn(button_down, 1)
        Controls.Grid.SetRow(button_down, 1)

        button_up.VerticalContentAlignment = WPF.VerticalAlignment.Center
        button_up.HorizontalContentAlignment = WPF.HorizontalAlignment.Center
        button_up.FontFamily = FontFamily('Marlett')
        button_up.FontSize = 8.0
        button_up.Content = 5
        button_up.Click += self.button_up_click

        # position button_up
        Controls.Grid.SetColumn(button_up, 1)
        Controls.Grid.SetRow(button_up, 0)

    def preview_key_down(self, sender: System.Object, eventargs: Input.KeyEventArgs) -> None:
        if eventargs.Key == Input.Key.Up:
            self.button_up.RaiseEvent(WPF.RoutedEventArgs(Controls.Button.ClickEvent))
            self.call_button_set_IsPressed(self.button_up, True)
        if eventargs.Key == Input.Key.Down:
            self.button_down.RaiseEvent(WPF.RoutedEventArgs(Controls.Button.ClickEvent))
            self.call_button_set_IsPressed(self.button_down, True)

    def preview_key_up(self, sender: System.Object, eventargs: Input.KeyEventArgs) -> None:
        if eventargs.Key == Input.Key.Up:
            self.call_button_set_IsPressed(self.button_up, False)
        if eventargs.Key == Input.Key.Down:
            self.call_button_set_IsPressed(self.button_down, False)

    def call_button_set_IsPressed(button: Controls.Button, value: bool) -> None:
        button.GetType().GetMethod("set_IsPressed", Reflection.BindingFlags.Instance | Reflection.BindingFlags.NonPublic).Invoke(button, [value])

    def text_changed(self, sender: Controls.TextBox, eventargs: Controls.TextChangedEventArgs) -> None:
        number = 0
        if self.text_box.Text:
            try:
                number = Decimal(self.text_box.Text)
            except ValueError:
                __logger__.error('Invalid numeric value entered in NumberInput control.')
                pass
        if self.interface.max_value and number > self.interface.max_value:
            self.text_box.Text = str(self.interface.max_value)
        if self.interface.min_value and number < self.interface.min_value:
            self.text_box.Text = str(self.interface.min_value)
        self.text_box.SelectionStart = len(self.text_box.Text)

    def button_down_click(self, sender: Controls.Button, eventargs: WPF.RoutedEventArgs) -> None:
        number = 0
        if self.text_box.Text:
            number = Decimal(self.text_box.Text)
            number = number - self.interface.step if self.interface.step else number
            if self.interface.min_value:
                number = self.interface.min_value if number > self.interface.min_value else number
        self.interface.value = number

    def button_up_click(self, sender: Controls.Button, eventargs: WPF.RoutedEventArgs) -> None:
        number = 0
        if self.text_box.Text:
            number = Decimal(self.text_box.Text)
            number = number + self.interface.step if self.interface.step else number
            if self.interface.max_value:
                number = self.interface.max_value if number > self.interface.max_value else number
        self.interface.value = number

    def set_readonly(self, value: bool):
        self.native.IsReadOnly = value

    def set_step(self, step: Decimal):
        __logger__.debug('Passing NumberInput.set_step.')
        pass

    def set_min_value(self, value: Decimal):
        __logger__.debug('Passing NumberInput.set_min_value.')
        pass

    def set_max_value(self, value: Decimal):
        __logger__.debug('Passing NumberInput.set_max_value.')
        pass

    def set_value(self, value: Decimal):
        self.text_box.Text = str(value)

    # def set_font(self, value):
    #     self._set_value('font', value)

    # def set_alignment(self, value):
    #     self._set_value('alignment', value)

    def set_on_change(self, handler):
        self.interface.factory.not_implemented('NumberInput.set_on_change')
