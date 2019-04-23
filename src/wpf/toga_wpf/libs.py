import clr
import sys
if sys.platform.lower() not in ['cli', 'win32']:
    print("WPF is only supported on Windows platform")
clr.AddReference("C:\\Windows\\Microsoft.NET\\assembly\\GAC_64\\PresentationCore\\v4.0_4.0.0.0__31bf3856ad364e35\\PresentationCore") # noqa: E501

import System  # noqa: W0611
import System.Windows as WPF  # noqa: W0611
from System import ArgumentException  # noqa: W0611
from System import Enum  # noqa: W0611
from System import Threading  # noqa: W0611
from System.Windows import Input  # noqa: W0611
from System.Windows import Media  # noqa: W0611
from System.Windows.Media import FontFamily  # noqa: W0611
from System.Windows.Media import SolidColorBrush  # noqa: W0611
