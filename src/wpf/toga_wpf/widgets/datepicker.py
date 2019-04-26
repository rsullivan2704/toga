import arrow
from toga.handlers import wrapped_handler
from toga_wpf.libs import Controls, System

from .base import Widget


class DatePicker(Widget):
    def create(self) -> None:
        self.native = Controls.DatePicker()

    def _get_dotnet_datetime(self, value: str) -> System.DateTime:  # noqa: E501
        v = arrow.get(value, 'YYYY-MM-DD HH:mm:ss:SSS').datetime
        return System.DateTime(v.year, v.month, v.day, v.hour, v.minute, v.second, (v.microsecond))  # noqa: E501

    def get_value(self) -> str:
        return self.native.SelectedDate

    def set_value(self, value: str) -> None:
        self.native.SelectedDate = self._get_dotnet_datetime(value)

    def set_min_date(self, value: str) -> None:
        self.native.DisplayDateStart = self._get_dotnet_datetime(value)

    def set_max_date(self, value: str) -> None:
        self.native.DisplayDateEnd = self._get_dotnet_datetime(value)

    def set_on_change(self, handler: type(wrapped_handler)) -> None:
        self.SelectedDateChanged += handler
