import toga
from .libs import WPF

CACHE = {}


def get_brush(c: toga.colors.Color) -> WPF.Media.SolidColorBrush:
    brush = WPF.Media.SolidColorBrush()
    try:
        color = CACHE[c]
    except KeyError:
        rgba = c.rgba()
        color = WPF.Media.Color.FromARGB(rgba.a, rgba.r, rgba.g, rgba.b)
        brush.Color = color
        CACHE[c] = brush
    return brush
