import shutil
from pathlib import Path

from maya import OpenMayaUI as omui
from maya import cmds

from uli_pipe.vendor.Qt import QtCore, QtWidgets

from .project_path import get_project_path

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance


def create_asset(name: str, asset_type: str, asset_dirpath: Path):
    # Create asset path
    asset_path = asset_dirpath / asset_type / name

    # Check if the asset_type is valid
    if asset_type not in ["character", "FX", "item", "prop", "set"]:
        raise ValueError(f"The asset type '{asset_type}' does not exist")
    # Check if the path exists and ends in "04_asset"
    if asset_dirpath.exists() is False:
        raise NotADirectoryError("The given asset directory path does not exist")
    if asset_dirpath.name != "04_asset":
        raise NameError("The end folder of the given asset directory path is not named '04_asset'")
    # Check if the name doesn't already exist at the asset path
    if asset_path.exists():
        raise NameError(f"There is already an asset named '{name}' in the assets directory")
    # Check if the name is not empty
    if len(name) == 0:
        raise NameError("Please provide a name for this asset")

    # Copy the asset template and paste it with the new name in the correct directory
    template_path = asset_dirpath / "_template_workspace_asset"
    shutil.copytree(template_path, asset_path)

    cmds.inViewMessage(
        message=f"<hl>Asset '{name}' has been created</hl>",
        position="midCenter",
        fade=True,
        fadeStayTime=3000,
        clickKill=True,
        dragKill=True,
    )
    return True


def create_shot(sequence_number: int, shot_number: int, shot_dirpath: Path):
    # Format the shot name (correct nomenclature)
    shot_name = f"sq{str(sequence_number).zfill(4)}_sh{str(shot_number).zfill(4)}"
    # Create shot path
    shot_path = shot_dirpath / shot_name

    # Check if the path exists and ends in "05_shot"
    if shot_dirpath.exists() is False:
        raise NotADirectoryError("The given shot directory path does not exist")
    if shot_dirpath.name != "05_shot":
        raise NameError("The end folder of the given shot directory path is not named '05_shot'")
    # Check if the shot name doesn't already exist at the shot path
    if shot_path.exists():
        raise NameError(f"There is already a shot named '{shot_name}' in the shot directory")

    # Copy the shot template and paste it with the new name in the correct directory
    template_path = shot_dirpath / "_template_workspace_shot"
    shutil.copytree(template_path, shot_path)

    cmds.inViewMessage(
        message=f"<hl>Shot '{shot_name}' has been created</hl>",
        pos="midCenter",
        fade=True,
        fadeStayTime=3000,
        clickKill=True,
        dragKill=True,
    )


def maya_main_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)


class CreateAsset(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Create Asset")
        self.setFixedHeight(150)
        self.setFixedWidth(255)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Create the widgets
        self.title = QtWidgets.QLabel("Asset Creator")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.asset_type = QtWidgets.QComboBox()
        self.asset_type.addItems(["character", "FX", "item", "prop", "set"])
        self.asset_name = QtWidgets.QLineEdit()
        self.asset_name.setPlaceholderText("Asset name...")
        self.create_button = QtWidgets.QPushButton("Create Asset")
        self.create_button.setFixedHeight(35)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.asset_choice_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.asset_choice_layout)
        self.main_layout.addWidget(self.create_button)
        self.asset_choice_layout.addWidget(self.asset_type)
        self.asset_choice_layout.addWidget(self.asset_name)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.create_button.clicked.connect(
            lambda: self.create_asset_and_close(
                name=self.asset_name.text(),
                asset_type=self.asset_type.currentText(),
            )
        )

    def create_asset_and_close(self, name: str, asset_type: str):
        # Call the backend function 'create_asset' and close the window afterward
        success = create_asset(
            name=name,
            asset_type=asset_type,
            asset_dirpath=get_project_path() / "04_asset",
        )
        if success is True:
            self.close()
            self.deleteLater()


class CreateShot(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=maya_main_window(), *args, **kwargs)
        self.setWindowTitle("Create Shot")
        self.setFixedHeight(165)
        self.setFixedWidth(320)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Create the widgets
        self.title = QtWidgets.QLabel("Shot Creator")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.sequence_number = QtWidgets.QDoubleSpinBox()
        self.sequence_number.setDecimals(1)
        self.sequence_number.setMinimum(1)
        self.shot_number = QtWidgets.QDoubleSpinBox()
        self.shot_number.setDecimals(1)
        self.shot_number.setMinimum(1)
        self.sequence_label = QtWidgets.QLabel("Sequence: ")
        self.sequence_label.setAlignment(QtCore.Qt.AlignRight)
        self.shot_label = QtWidgets.QLabel("Shot: ")
        self.shot_label.setAlignment(QtCore.Qt.AlignRight)
        self.create_button = QtWidgets.QPushButton("Create Shot")
        self.create_button.setFixedHeight(35)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.shot_choice_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.shot_choice_layout)
        self.main_layout.addWidget(self.create_button)
        self.shot_choice_layout.addWidget(self.sequence_label)
        self.shot_choice_layout.addWidget(self.sequence_number)
        self.shot_choice_layout.addWidget(self.shot_label)
        self.shot_choice_layout.addWidget(self.shot_number)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.create_button.clicked.connect(
            lambda: self.create_shot_and_close(
                sequence_number=int(self.sequence_number.value() * 10),
                shot_number=int(self.shot_number.value() * 10),
            )
        )

    def create_shot_and_close(self, sequence_number, shot_number):
        # Call the backend function 'create_shot' and close the window afterward
        success = create_shot(
            sequence_number=sequence_number,
            shot_number=shot_number,
            shot_dirpath=get_project_path() / "05_shot",
        )
        if success is True:
            self.close()
            self.deleteLater()
