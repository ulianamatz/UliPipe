import shutil
from pathlib import Path

from maya import OpenMayaUI as omui
from maya import cmds
from uli_pipe.vendor.Qt import QtCore, QtWidgets
from uli_pipe.vendor.Qt.QtWidgets import QLabel
from shiboken6 import wrapInstance

from .project_path import get_project_path


# Backend ---------------------------------------------------------------------
def open_scene(scene_path: Path):
    # Check if current scene has changes
    if cmds.file(q=True, modified=True):
        # Prompt user to save
        result = cmds.confirmDialog(title="Save Changes", message="Save changes to current scene?", button=["Save", "Don't Save", "Cancel"], defaultButton="Save", cancelButton="Cancel", dismissString="Cancel")
        if result == "Save":
            cmds.file(save=True)
        elif result == "Cancel":
            return False
    # Open the new file
    cmds.file(scene_path, open=True, force=True)
    return True


def open_asset(name: str, asset_type: str, department: str, version_file: str, asset_dirpath: Path):
    # Create the path to the scene directory
    scene_dirpath = asset_dirpath / asset_type / name / "maya" / "scenes" / "edit" / department
    # Check if the path exists
    if not scene_dirpath.exists():
        raise NotADirectoryError(f"The path '{scene_dirpath}' to the asset '{name}' does not exist")

    # Check if there is a scene in the directory, if not create it, if yes pick the latest version
    dir_paths = list(scene_dirpath.iterdir())
    dir_files = [i.stem for i in dir_paths]
    # IF no files, create the first one
    if len(dir_files) == 0:
        first_file_name = f"{name.lower()}_{department}_E_001.ma"
        first_file_path = scene_dirpath / first_file_name
        # Get the template scene path
        template_path = Path(__file__).parent / "assets" / "scene_template.ma"
        shutil.copyfile(template_path, first_file_path)
        open_path = first_file_path
        cmds.inViewMessage(message=f"Directory empty: created the scene <hl>{first_file_name}</hl>", pos="midCenter", fade=True, fadeStayTime=3000, clickKill=True, dragKill=True)
    else:
        open_path = scene_dirpath / version_file
        if not open_path.exists():
            raise FileExistsError(f"The version '{version_file}' does not exist")

    # Open the scene
    open_scene(scene_path=open_path)


def open_shot(name: str, department: str, shot_dirpath: Path, version_file: str):
    # Create the path to the scene directory
    scene_dirpath = shot_dirpath / name / "maya" / "scenes" / department / "edit"
    # Check if the path exists
    if not scene_dirpath.exists():
        raise NotADirectoryError(f"The path '{scene_dirpath}' to the shot '{name}' does not exist")

    # Check if there is a scene in the directory, if not create it, if yes pick the latest version
    dir_paths = list(scene_dirpath.iterdir())
    dir_files = [i.stem for i in dir_paths]
    # IF no files, create the first one
    if len(dir_files) == 0:
        first_file_name = f"{name.lower()}_{department}_E_001.ma"
        first_file_path = scene_dirpath / first_file_name
        # Get the template scene path
        template_path = Path(__file__).parent / "assets" / "scene_template.ma"
        shutil.copyfile(template_path, first_file_path)
        open_path = first_file_path
        cmds.inViewMessage(message=f"Directory empty: created the scene <hl>{first_file_name}</hl>", pos="midCenter", fade=True, fadeStayTime=3000, clickKill=True, dragKill=True)
    else:
        open_path = scene_dirpath / version_file
        if not open_path.exists():
            raise FileExistsError(f"The version '{version_file}' does not exist")

    # Open the scene
    open_scene(scene_path=open_path)


# Frontend -----------------------------------------------------------------------
def maya_main_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)


class OpenAsset(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Open Asset")
        # self.setFixedHeight(150)
        # self.setFixedWidth(255)

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
        self.asset_version_label = QLabel("Version: ")
        self.asset_version_label.setAlignment(QtCore.Qt.AlignRight)

        # Create the combo boxes
        self.asset_type = QtWidgets.QComboBox()
        self.asset_type.addItems(["character", "FX", "item", "prop", "set"])
        self.department = QtWidgets.QComboBox()
        self.department.addItems(["assetLayout", "cloth", "dressing", "groom", "lookdev", "modeling", "rig"])
        self.asset_name = QtWidgets.QComboBox()
        self.update_assets_names()
        self.asset_version = QtWidgets.QComboBox()
        self.update_assets_versions()

        # Create the open button
        self.open_button = QtWidgets.QPushButton("Open Asset")
        self.open_button.setFixedHeight(35)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Asset type layout
        self.asset_type_layout = QtWidgets.QHBoxLayout()
        self.asset_type_layout.addWidget(self.asset_type_label)
        self.asset_type_layout.addWidget(self.asset_type)

        # Asset name layout
        self.asset_name_layout = QtWidgets.QHBoxLayout()
        self.asset_name_layout.addWidget(self.asset_name_label)
        self.asset_name_layout.addWidget(self.asset_name)

        # Department layout
        self.department_layout = QtWidgets.QHBoxLayout()
        self.department_layout.addWidget(self.department_label)
        self.department_layout.addWidget(self.department)

        # Version layout
        self.asset_version_layout = QtWidgets.QHBoxLayout()
        self.asset_version_layout.addWidget(self.asset_version_label)
        self.asset_version_layout.addWidget(self.asset_version)

        # Add everything to the main layout
        self.main_layout.addLayout(self.asset_type_layout)
        self.main_layout.addLayout(self.asset_name_layout)
        self.main_layout.addLayout(self.department_layout)
        self.main_layout.addLayout(self.asset_version_layout)
        self.main_layout.addWidget(self.open_button)

    def create_connections(self):
        self.asset_type.currentIndexChanged.connect(lambda: self.update_assets_names())
        self.asset_name.currentIndexChanged.connect(lambda: self.update_assets_versions())
        self.department.currentIndexChanged.connect(lambda: self.update_assets_versions())
        self.open_button.clicked.connect(lambda: self.open_asset_and_close(name=self.asset_name.currentText(), department=self.department.currentText(), asset_type=self.asset_type.currentText(), version_file=self.asset_version.currentText()))

    def open_asset_and_close(self, name: str, department: str, asset_type: str, version_file: str):
        # Call the backend function 'open_asset' and close the window afterward
        success = open_asset(name=name, department=department, asset_type=asset_type, asset_dirpath=get_project_path() / "04_asset", version_file=version_file)
        if success is True:
            self.close()
            self.deleteLater()

    def update_assets_names(self):
        assets_path = get_project_path() / "04_asset" / self.asset_type.currentText()
        assets_names = [i.stem for i in assets_path.iterdir()]
        self.asset_name.clear()
        self.asset_name.addItems(assets_names)

    def update_assets_versions(self):
        asset_path = get_project_path() / "04_asset" / self.asset_type.currentText() / self.asset_name.currentText() / "maya" / "scenes" / "edit" / self.department.currentText()
        versions_names = [i.name for i in asset_path.iterdir()]
        self.asset_version.clear()
        self.asset_version.addItems(versions_names)
        self.asset_version.setCurrentIndex(len(versions_names) - 1)


class OpenShot(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Open Shot")
        # self.setFixedHeight(150)
        # self.setFixedWidth(255)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Create the labels
        self.shot_name_label = QLabel("Shot name: ")
        self.shot_name_label.setAlignment(QtCore.Qt.AlignRight)
        self.department_label = QLabel("Department: ")
        self.department_label.setAlignment(QtCore.Qt.AlignRight)
        self.shot_version_label = QLabel("Version: ")
        self.shot_version_label.setAlignment(QtCore.Qt.AlignRight)

        # Create the combo boxes
        self.department = QtWidgets.QComboBox()
        self.department.addItems(["anim", "layout", "render"])
        self.shot_name = QtWidgets.QComboBox()
        self.update_shots_names()
        self.shot_version = QtWidgets.QComboBox()
        self.update_shots_versions()

        # Create the open button
        self.open_button = QtWidgets.QPushButton("Open Asset")
        self.open_button.setFixedHeight(35)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Asset name layout
        self.shot_name_layout = QtWidgets.QHBoxLayout()
        self.shot_name_layout.addWidget(self.shot_name_label)
        self.shot_name_layout.addWidget(self.shot_name)

        # Department layout
        self.department_layout = QtWidgets.QHBoxLayout()
        self.department_layout.addWidget(self.department_label)
        self.department_layout.addWidget(self.department)

        # Version layout
        self.shot_version_layout = QtWidgets.QHBoxLayout()
        self.shot_version_layout.addWidget(self.shot_version_label)
        self.shot_version_layout.addWidget(self.shot_version)

        # Add everything to the main layout
        self.main_layout.addLayout(self.shot_name_layout)
        self.main_layout.addLayout(self.department_layout)
        self.main_layout.addLayout(self.shot_version_layout)
        self.main_layout.addWidget(self.open_button)

    def create_connections(self):
        self.open_button.clicked.connect(lambda: self.open_shot_and_close(name=self.shot_name.currentText(), department=self.department.currentText(), version_file=self.shot_version.currentText()))
        self.shot_name.currentIndexChanged.connect(lambda: self.update_shots_versions())
        self.department.currentIndexChanged.connect(lambda: self.update_shots_versions())

    def open_shot_and_close(self, name: str, department: str, version_file: str):
        # Call the backend function 'open_asset' and close the window afterward
        success = open_shot(name=name, department=department, shot_dirpath=get_project_path() / "05_shot", version_file=version_file)
        if success is True:
            self.close()
            self.deleteLater()

    def update_shots_names(self):
        shots_path = get_project_path() / "05_shot"
        shots_names = [i.stem for i in shots_path.iterdir()]
        shots_names = [i for i in shots_names if i.startswith("sq")]
        self.shot_name.clear()
        self.shot_name.addItems(shots_names)

    def update_shots_versions(self):
        shot_path = get_project_path() / "05_shot" / self.shot_name.currentText() / "maya" / "scenes" / self.department.currentText() / "edit"
        versions_names = [i.name for i in shot_path.iterdir()]
        self.shot_version.clear()
        self.shot_version.addItems(versions_names)
        self.shot_version.setCurrentIndex(len(versions_names) - 1)
