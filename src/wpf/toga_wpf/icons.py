import os
import toga
from toga_wpf.libs import System
from toga_wpf.libs import Imaging


class Icon:

    EXTENSIONS = ('.bmp', '.ico', 'png')

    def __init__(self, interface: toga.Icon) -> None:
        self.interface = interface
        file_path, file_extension = (os.path.splitext(self.interface.filename))
        if file_extension in self.EXTENSIONS:
            self.native = Imaging.BitmapFrame().Create(System.Uri(self.interface.filename, System.UriKind.RelativeOrAbsolute))  # noqa: E501
