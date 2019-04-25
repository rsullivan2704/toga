import os

import toga
from toga_wpf.libs import WPF, Imaging, System


class Image(object):

    EXTENSIONS = ('.bmp', '.gif', '.ico', '.jpg', 'png', '.wdp', '.tiff')

    def __init__(self, interface: toga.Image):
        self.interface = interface
        self.native = WPF.Controls.Image()

    def load_image(self, path: str) -> None:
        file_path, file_extension = os.path.splitext(path)
        bi = Imaging.BitmapImage()
        if file_extension in self.EXTENSIONS:
            bi.BeginInit()
            bi.UriSource = System.Uri(path, System.UriKind.RelativeOrAbsolute)  # noqa: E501
            bi.EndInit()
            self.native.Source = bi
