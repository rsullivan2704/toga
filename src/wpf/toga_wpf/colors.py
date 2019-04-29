import toga
from .libs import Color, SolidColorBrush

CACHE = {}


def get_brush(c: toga.colors.Color) -> SolidColorBrush:
    brush = SolidColorBrush()
    try:
        brush = CACHE[c]
    except KeyError:
        rgba = c.rgba()
        color = Color.FromARGB(rgba.a, rgba.r, rgba.g, rgba.b)
        brush.Color = color
        CACHE[c] = brush
    return brush
