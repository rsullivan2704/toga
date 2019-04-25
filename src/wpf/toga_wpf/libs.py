import os
import sys

import clr

if sys.platform.lower() not in ['cli', 'win32']:
    print("WPF is only supported on Windows platform")
windir = os.environ['WINDIR']
# clr.AddReference('{dir}\\Microsoft.NET\\Framework64\\v4.0.30319\\WPF\\PresentationFramework.dll'.format(dir=windir)) # noqa: E501
clr.AddReference(r"wpf\PresentationFramework") # noqa: E501

import System  # noqa: W0611
import System.Windows as WPF  # noqa: W0611
from System import ArgumentException  # noqa: W0611
from System import Enum  # noqa: W0611
from System import Threading  # noqa: W0611
from System.Windows import Input  # noqa: W0611
from System.Windows.Media import Imaging  # noqa: W0611
from System.Windows.Media import FontFamily  # noqa: W0611
from System.Windows.Media import SolidColorBrush  # noqa: W0611


def add_handler(action):

    def handler(sender, event):
        return action(None)

    return handler
