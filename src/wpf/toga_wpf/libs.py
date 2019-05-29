import sys
import logging

__logger__ = logging.getLogger('toga_wpf_logger')
__logger__.setLevel(logging.DEBUG)
__ch__ = logging.StreamHandler()
__ch__.setLevel(logging.DEBUG)
__formatter__ = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
__ch__.setFormatter(__formatter__)
__logger__.addHandler(__ch__)

import clr  # noqa: E402

if sys.platform.lower() not in ['cli', 'win32']:
    print("WPF is only supported on Windows platform")
clr.AddReference(r"wpf\PresentationFramework")

import System  # noqa: E402
import System.Windows as WPF    # noqa: E402, W0611
from System import ArgumentException, Enum, Threading  # noqa: W0611
from System.Drawing import Brushes  # noqa: W0611
from System.Globalization import CultureInfo  # noqa: W0611
from System.Windows import Controls, Data, FontStretches, Input  # noqa: W0611
from System.Windows.Media import Imaging, FontFamilyConverter, FontFamily, FormattedText, NumberSubstitution, Typeface, Color, Colors, SolidColorBrush, VisualTreeHelper  # noqa: W0611, E501


def add_handler(action):

    def handler(sender, event):
        return action(None)

    return handler
