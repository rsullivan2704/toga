from toga_wpf.widgets.textinput import TextInput
from toga_wpf.libs import WPF, Controls


class MultilineTextInput(TextInput):
    def create(self) -> None:
        super().create()
        self.native.AcceptsReturn = True
        self.native.HorizontalScrollBarVisibility = Controls.ScrollBarVisibility.Disabled
        self.native.VerticalScrollBarVisibility = Controls.ScrollBarVisibility.Auto
        self.native.TextWrapping = WPF.TextWrapping.Wrap
