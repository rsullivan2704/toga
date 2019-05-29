from toga_wpf.libs import WPF


class WPFViewport:
    def __init__(self, native: WPF.FrameworkElement, frame: object) -> None:
        self.native = native
        self.frame = frame
        self.BASE_DPI = 96
        self._dpi = self.BASE_DPI

    @property
    def dpi(self) -> float:
        return self._dpi

    @property
    def width(self) -> float:
        return self.native.Content.ActualWidth

    @property
    def height(self) -> float:
        return self.native.Content.ActualHeight
