import importlib
import os
import shutil
import sys
from pathlib import Path

from maya import cmds


MAYA_APP_DIR = os.getenv("MAYA_APP_DIR")
SUPPORTED_MAYA_VERSIONS = (2023, 2024, 2025)

MODULE_VERSION = "0.1.0"
MODULE_NAME = "UliPipe"
REPOSITORY_DIR = Path(__file__).parent / "UliPipe"
ICONS_FOLDER_NAME = "UliPipe-icons"


def mod_contents():
    """Creates the .mod file's contents with the provided info."""

    mod_contents_str = ""

    for maya_version in SUPPORTED_MAYA_VERSIONS:
        to_append_str = f"""+ MAYAVERSION:{maya_version} {MODULE_NAME} {MODULE_VERSION} {Path(MAYA_APP_DIR).as_posix()}/modules/{MODULE_NAME}
plug-ins: plug-ins
icons: icons
[r] scripts: scripts

"""
        mod_contents_str += to_append_str
    return mod_contents_str


def install_mod():
    """Installs the module by creating a .mod file in the Maya modules directory
    with the parent's directory as the path, and by copying/replacing the module into Maya's module folder.
    Also installs the icons in the correct directory.
    """

    # Create the .mod file
    target_mod_filepath = Path(MAYA_APP_DIR) / "modules" / f"{MODULE_NAME}.mod"
    target_mod_filepath.parent.mkdir(parents=True, exist_ok=True)
    # Write the module contents inside it
    target_mod_filepath.write_text(mod_contents())

    # delete the UliPipe folder in the maya modules directory if it exists
    modules_dirpath = Path(MAYA_APP_DIR) / "modules"
    uli_dirpath = modules_dirpath / MODULE_NAME
    if uli_dirpath.exists() is True:
        shutil.rmtree(uli_dirpath)

    # Copy the repo dir and its contents to the modules directory and rename it to UliPipe
    shutil.copytree(REPOSITORY_DIR, uli_dirpath)

    # Copy the shelf icons to the icons dir
    icons_dirpath = REPOSITORY_DIR.parent / "assets" / ICONS_FOLDER_NAME
    for version in SUPPORTED_MAYA_VERSIONS:
        version_path = Path(MAYA_APP_DIR) / str(version)
        if version_path.exists():
            maya_icons_dir = version_path / "prefs" / "icons" / ICONS_FOLDER_NAME
            shutil.copytree(icons_dirpath, maya_icons_dir, dirs_exist_ok=True)


def load_user_setup():
    """Adds the module to the sys.path and imports the userSetup.py file (if it
    exists) manually for the current session. On the next startup, these will be
    loaded automatically."""

    scripts_dir = REPOSITORY_DIR.joinpath("scripts")
    user_setup = scripts_dir.joinpath("userSetup.py")

    if scripts_dir.exists():
        if scripts_dir not in sys.path:
            sys.path.append(scripts_dir.as_posix())

        if user_setup.exists():
            spec = importlib.util.spec_from_file_location(user_setup.stem, user_setup.as_posix())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


def onMayaDroppedPythonFile(*args, **kwargs):
    """Callback function to be executed when a Python file is dropped into the Maya
    viewport. It reloads the current module, installs the module, and loads the
    userSetup.py file."""

    self_import = importlib.import_module(__name__)
    importlib.reload(self_import)

    self_import.install_mod()
    self_import.load_user_setup()

    from uli_pipe import reload_module
    reload_module()

    cmds.confirmDialog(
        title="UliPipe Installation",
        message="UliPipe installed successfully.",
        button="OK",
        defaultButton="OK",
        cancelButton="OK",
    )
