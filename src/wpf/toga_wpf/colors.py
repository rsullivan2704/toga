import toga
from .libs import Color, SolidColorBrush

CACHE = {}


def native_color(c: toga.colors.Color) -> SolidColorBrush:
    brush = SolidColorBrush()
    try:
        brush = CACHE[c]
    except KeyError:
        rgba = c.rgba
        color = Color.FromArgb(rgba.a, rgba.r, rgba.g, rgba.b)
        brush.Color = color
        CACHE[c] = brush
    return brush
