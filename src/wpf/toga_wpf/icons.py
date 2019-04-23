import os
import toga
from toga_wpf.libs import System, WPF
from toga_wpf.libs.Media import Imaging


class Icon:
    def __init__(self, interface: toga.Icon) -> None:
        self.interface = interface
        self.interface._impl = self
        valid_extensions = ('.bmp', '.gif', '.ico', '.jpg', 'png', '.wdp', '.tiff')  # noqa: E501
        file_path, file_extension = os.path.splitext(self.interface.filename)
        bi = Imaging.BitmapImage()
        if file_extension in valid_extensions:
            bi.BeginInit()
            bi.UriSource = System.Uri(self.interface.filename, System.UriKind.RelativeOrAbsolute)  # noqa: E501
            bi.EndInit()
        self.native = WPF.Controls.Image()
        self.native.Source = bi
