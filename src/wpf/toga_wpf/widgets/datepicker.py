from datetime import date, datetime
from toga.handlers import wrapped_handler
from toga_wpf.libs import Controls, System

from .base import Widget


class DatePicker(Widget):
    def create(self) -> None:
        self.native = Controls.DatePicker()
        self.native.SelectedDateFormat = Controls.DatePickerFormat.Long

    def get_value(self) -> date:
        return datetime.strptime(self.native.Text, '%A, %B %d, %Y').date()

    def set_value(self, value: str) -> None:
        date_value = System.DateTime.Parse(value)
        start_date = self.native.DisplayDateStart
        end_date = self.native.DisplayDateEnd
        if start_date and date_value < start_date:
            date_value = start_date
        if end_date and date_value > end_date:
            date_value = end_date
        self.native.SelectedDate = date_value

    def set_min_date(self, value: str) -> None:
        start_date = System.DateTime.Parse(value)
        # Have to check and set the SelectedDate if it is less than
        # the min date as it will automatically extend the min date
        if self.native.SelectedDate < start_date:
            self.native.SelectedDate = start_date
        self.native.DisplayDateStart = start_date

    def set_max_date(self, value: str) -> None:
        end_date = System.DateTime.Parse(value)
        # Have to check and set the SelectedDate if it is greater than
        # the max date as it will automatically extend the max date
        if self.native.SelectedDate > end_date:
            self.native.SelectedDate = end_date
        self.native.DisplayDateEnd = end_date

    def set_on_change(self, handler: type(wrapped_handler)) -> None:
        self.native.SelectedDateChanged += self.on_date_changed

    def on_date_changed(self, sender: object, event: Controls.SelectionChangedEventArgs) -> None:  # noqa: E501
        if self.interface.on_change:
            self.interface.on_change(self.interface)
