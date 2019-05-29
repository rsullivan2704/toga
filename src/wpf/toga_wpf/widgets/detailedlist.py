import toga

from toga_wpf.widgets.base import Widget
from toga_wpf.libs import Controls, __logger__


class WPFDataGrid(Controls.DataGrid):
    def __init__(self, interface: toga.DetailedList) -> None:
        super().__init__()
        self.interface = interface
        self.SelectionChanged += self.on_selection_changed

    def on_selection_changed(self, sender: Controls.ListBox, eventargs: Controls.SelectionChangedEventArgs) -> None:
        try:
            self.interface.on_select(self.interface)
        except AttributeError as ex:
            __logger__.info('Passing AttributeError in WPFListBox.on_selection_changed\n{message}'.format(message=str(ex)))
            pass
        except TypeError:
            __logger__.info('DetailedList.on_select handler not defined.')
            pass


class DetailedList(Widget):
    def create(self):
        self.native = WPFDataGrid(self.interface)

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, item: toga.Widget):
        self.native.ItemSource.Add(item)

    def change(self, item):
        self._action('change', item=item)

    def remove(self, item):
        self._action('remove', item=item)

    def clear(self):
        self._action('clear')

    def set_on_refresh(self, handler):
        self._set_value('on_refresh', handler)

    def after_on_refresh(self):
        self._action('after on refresh')

    def set_on_delete(self, handler):
        self._set_value('on_delete', handler)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def scroll_to_row(self, row):
        item = self.native.Items.GetItemAt(row)
        self.native.ScrollIntoView(item)
