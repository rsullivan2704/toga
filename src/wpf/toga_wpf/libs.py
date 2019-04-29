import sys

import clr

if sys.platform.lower() not in ['cli', 'win32']:
    print("WPF is only supported on Windows platform")
clr.AddReference(r"wpf\PresentationFramework")

import System  # noqa: W0611
import System.Windows as WPF  # noqa: W0611
from System import ArgumentException, Enum, Threading  # noqa: W0611
from System.Drawing import Brushes  # noqa: W0611
from System.Globalization import CultureInfo  # noqa: W0611
from System.Windows import Controls, FontStretches, Input  # noqa: W0611
from System.Windows.Media import Imaging, FontFamilyConverter, FontFamily, FormattedText, NumberSubstitution, Typeface, Color, SolidColorBrush  # noqa: W0611, E501


def add_handler(action):

    def handler(sender, event):
        return action(None)

    return handler


def get_clr_type(typ):
    """ simulate typeof(T) or GetClrType from IronPython.

    Horrible hack, redo
    """
    name = typ.__module__ + "." + typ.__name__
    return System.Type.GetType(name)
