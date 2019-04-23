import toga
from .libs.Media import Color
from .libs.Media import SolidColorBrush

CACHE = {}


def get_brush(self, c: toga.colors.Color) -> SolidColorBrush:
    brush = SolidColorBrush()
    try:
        color = CACHE[c]
    except KeyError:
        rgba = c.rgba()
        color = Color.FromARGB(rgba.a, rgba.r, rgba.g, rgba.b)
        brush.Color = color
        CACHE[c] = brush
    return brush
