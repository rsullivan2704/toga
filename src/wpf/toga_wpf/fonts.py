
from collections import namedtuple

import toga
from toga_wpf.libs import (WPF, Brushes, CultureInfo, Enum,
                           FontFamilyConverter, FontStretches, FormattedText,
                           NumberSubstitution, System, Typeface, __logger__)  # , get_clr_type)

_FONT_CACHE = {}


class Font:
    def __init__(self, interface: toga.Font) -> None:
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font = namedtuple('dotnetFont', ['typeface', 'size', 'variant'])  # noqa: E501

            font_family_conv = FontFamilyConverter()
            family = font_family_conv.ConvertFromInvariantString(self.interface.family)  # noqa: E501

            font_style_conv = WPF.FontStyleConverter()
            style = font_style_conv.ConvertFromInvariantString(self.interface.style)  # noqa: E501

            font_weight_conv = WPF.FontWeightConverter()
            weight = font_weight_conv.ConvertFromInvariantString(self.interface.weight)  # noqa: E501

            font.typeface = Typeface(family, style, weight, FontStretches.Medium)  # noqa: E501

            font_size_conv = WPF.FontSizeConverter()
            font.size = font_size_conv.ConvertFromInvariantString(str(self.interface.size))  # noqa: E501

            font.variant = None
            # TODO: have to get the FontCapitals clr type
            # to use when parsing the enum value
            # clr.GetClrType(typ) has not been implemented on the PyPI
            # distro of pythonnet due to an unresolved numpy issue
            # capitals_enum = clr.GetClrType(WPF.FontCapitals)
            try:
                font.variant = Enum.Parse(WPF.FontCapitals, self.interface.variant, True)  # noqa: E501
            except (AttributeError, System.ArgumentNullException, ArgumentExcetption, OverflowException) as ex:  # noqa: E501
                __logger__.debug('Error parsing System.Windows.FontCapitals enumerated value.\nValue: {value}\n{exception}'.format(value=self.interface.value, exception=ex))  # noqa: E501

            _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text: str, tight: bool = False) -> tuple:
        formatted_text = FormattedText(
            text,
            CultureInfo.CurrentCulture,
            WPF.FlowDirection.LeftToRight,
            self.native.typeface,
            self.native.size,
            Brushes.Black,
            NumberSubstitution(),
            1
        )
        return formatted_text.Width, formatted_text.Height
