import random
from pathlib import Path

from maya import OpenMayaUI as omui

from uli_pipe.vendor.Qt import QtCore, QtGui, QtWidgets

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance


def maya_main_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)


class SillyPopup(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Motivational Popup")
        self.setFixedHeight(625)
        self.setFixedWidth(850)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Create the image widget
        raw_image_pixmap = QtGui.QPixmap(get_random_image().as_posix())
        self.image_pixmap = raw_image_pixmap.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(self.image_pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create the buttons
        self.thank_you_button = QtWidgets.QPushButton("Thank You!")
        self.more_button = QtWidgets.QPushButton("More Please!")

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.thank_you_button)
        self.buttons_layout.addWidget(self.more_button)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.thank_you_button.clicked.connect(self.close_popup)
        self.more_button.clicked.connect(self.update_image)

    def close_popup(self):
        self.close()

    def update_image(self):
        raw_image_pixmap = QtGui.QPixmap(get_random_image().as_posix())
        self.new_pixmap = raw_image_pixmap.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.image_label.setPixmap(self.new_pixmap)


def get_random_image():
    secret_path = Path(__file__).parent / "assets" / "secret_do_not_open"
    # Get a list of all the files
    files = [file for file in secret_path.iterdir() if file.is_file()]
    # Pick one at random
    random_path = random.choice(files)
    return random_path
