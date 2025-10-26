from pathlib import Path

from maya import cmds
from uli_pipe.vendor.Qt import QtWidgets


def set_project_path():
    # Query the current project path (we do it first in case the user cancel the action of setting the new path)
    new_project_path = Path(QtWidgets.QFileDialog.getExistingDirectory())
    print(new_project_path)

    # Continue only if the user didn't cancel the operation
    if new_project_path != Path("."):
        # check if the path to .ulipipe exists, else create it
        ulipipe_path = Path.home() / ".ulipipe"
        if ulipipe_path.exists() is False:
            ulipipe_path.mkdir()

        # Same for the current_project file inside .ulipipe
        current_project_path = ulipipe_path / "current_project.txt"
        if current_project_path.exists() is False:
            current_project_path.touch()

        # Save this path as a string in the file
        with open(current_project_path, "w") as file:
            file.write(new_project_path.as_posix())

        cmds.inViewMessage(message=f"<hl>Project '{new_project_path.name}' has been set</hl>", pos="midCenter", fade=True, fadeStayTime=3000, clickKill=True, dragKill=True)
        return new_project_path
    return None


def get_project_path():
    # Create the Path object to the current_project file
    current_project_path = Path.home() / ".ulipipe" / "current_project.txt"
    # If it doesn't exist output an error
    if current_project_path.exists() is False:
        raise FileNotFoundError("The current_project file does not exist, please use the Set Project Path beforehand")
    # if it exists, read its content
    with open(current_project_path, "r") as file:
        file_data = file.read()

    # If the file is empty raise an error
    if len(file_data) == 0:
        raise ValueError("The current_project file does not contain a path to a project, please use the Set Project Path beforehand")
    # If the file has a path, return it
    return Path(file_data)
