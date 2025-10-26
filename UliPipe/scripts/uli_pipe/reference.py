from pathlib import Path

from uli_pipe.vendor.Qt import QtWidgets, QtCore
from uli_pipe.vendor.Qt.QtWidgets import QLabel
from shiboken6 import wrapInstance
from maya import OpenMayaUI as omui
from maya import cmds

from uli_pipe.project_path import get_project_path


# Backend ---------------------------------------------------------------------
def reference_scene(scene_path: Path):
    # Reference the new file
    cmds.file(scene_path, reference=True, force=True, namespace=scene_path.stem)
    return True


def reference_asset(name: str, asset_type: str, department: str, asset_dirpath: Path):
    # Create the path to the scene directory
    scene_dirpath = asset_dirpath / asset_type / name / "maya" / "scenes" / "publish" / department
    # Check if the path exists
    if not scene_dirpath.exists():
        raise NotADirectoryError(f"The path '{scene_dirpath}' to the asset '{name}' does not exist")

    # Get a list of the files in the directory
    dir_paths = list(scene_dirpath.iterdir())
    files_paths = []
    for i in dir_paths:
        if i.is_file() is True:
            files_paths.append(i)
    filenames = []
    for i in files_paths:
        filenames.append(i.stem)

    # Get all the files that end in _P
    publish_files = []
    for filename in filenames:
        if filename.endswith("_P") is True:
            publish_files.append(filename)

    # IF no publish files or multiple, return errors, ELSE continue
    if len(publish_files) == 0:
        raise FileNotFoundError(f"There is no publish file in the directory '{scene_dirpath}'")
    elif len(publish_files) > 1:
        raise FileNotFoundError(f"There are multiple conflicting publish files in the directory '{scene_dirpath}'")
    else:
        reference_index = filenames.index(publish_files[0])
        reference_path = files_paths[reference_index]

    # Open the scene
    success = reference_scene(scene_path=reference_path)
    return success


# Frontend -----------------------------------------------------------------------
def maya_main_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)


class ReferenceAsset(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Reference Asset")
        #self.setFixedHeight(150)
        #self.setFixedWidth(255)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Create the labels
        self.asset_type_label = QLabel("Asset type: ")
        self.asset_type_label.setAlignment(QtCore.Qt.AlignRight)
        self.asset_name_label = QLabel("Asset name: ")
        self.asset_name_label.setAlignment(QtCore.Qt.AlignRight)
        self.department_label = QLabel("Department: ")
        self.department_label.setAlignment(QtCore.Qt.AlignRight)

        # Create the combo boxes
        self.asset_type = QtWidgets.QComboBox()
        self.asset_type.addItems(["character", "FX", "item", "prop", "set"])
        self.department = QtWidgets.QComboBox()
        self.department.addItems(["assetLayout", "cloth", "dressing", "groom", "lookdev", "modeling", "rig"])
        self.asset_name = QtWidgets.QComboBox()
        self.update_assets_names()

        # Create the open button
        self.open_button = QtWidgets.QPushButton("Reference Asset")
        self.open_button.setFixedHeight(35)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Asset type layout
        self.asset_type_layout = QtWidgets.QHBoxLayout()
        self.asset_type_layout.addWidget(self.asset_type_label)
        self.asset_type_layout.addWidget(self.asset_type)
        self.main_layout.addLayout(self.asset_type_layout)

        # Asset name layout
        self.asset_name_layout = QtWidgets.QHBoxLayout()
        self.asset_name_layout.addWidget(self.asset_name_label)
        self.asset_name_layout.addWidget(self.asset_name)
        self.main_layout.addLayout(self.asset_name_layout)

        # Department layout
        self.department_layout = QtWidgets.QHBoxLayout()
        self.department_layout.addWidget(self.department_label)
        self.department_layout.addWidget(self.department)
        self.main_layout.addLayout(self.department_layout)

        # Add everything to the main layout
        self.main_layout.addLayout(self.asset_type_layout)
        self.main_layout.addLayout(self.asset_name_layout)
        self.main_layout.addLayout(self.department_layout)
        self.main_layout.addWidget(self.open_button)

    def create_connections(self):
        self.asset_type.currentIndexChanged.connect(lambda: self.update_assets_names())
        self.open_button.clicked.connect(lambda: self.reference_asset_and_close(name=self.asset_name.currentText(), department=self.department.currentText(), asset_type=self.asset_type.currentText()))

    def reference_asset_and_close(self, name: str, department: str, asset_type: str):
        # Call the backend function 'open_asset' and close the window afterward
        success = reference_asset(name=name, department=department, asset_type=asset_type, asset_dirpath=get_project_path() / "04_asset")
        if success is True:
            self.close()
            self.deleteLater()

    def update_assets_names(self):
        assets_path = get_project_path() / "04_asset" / self.asset_type.currentText()
        assets_names = [i.stem for i in assets_path.iterdir()]
        self.asset_name.clear()
        self.asset_name.addItems(assets_names)
