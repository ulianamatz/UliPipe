# Order convention for imports: Python base libraries, third-party libraries, your own libraries
from pathlib import Path

from maya import cmds
from uli_pipe.project_path import get_project_path


def save_edit():
    # Get the path to the project
    project_path = get_project_path()

    # Get a path to the current file (in Maya)
    current_file = cmds.file(query=True, sceneName=True)
    if len(current_file) == 0:
        raise FileExistsError("The current Maya scene is not in any file, please save the file, before saving an increment")
    else:
        current_file = Path(current_file)

    # Check if the current file is located inside the current project
    if current_file.is_relative_to(project_path) is False:
        # IF not, raise an error
        raise RuntimeError("The current Maya file is not located within the current project, please set the correct project")

    # Get its name and increment it
    current_scene_name = current_file.stem
    scene_extension = current_file.suffix
    name_parts = current_scene_name.split("_E_")
    if len(name_parts) != 2:
        raise NameError("The file name doesn't follow the format: 'name'_E_'number'")
    new_number = str(int(name_parts[1]) + 1).zfill(3)
    new_name = f"{name_parts[0]}_E_{new_number}"

    # Recreate the path
    new_path = current_file.parent / (new_name + scene_extension)
    # Raise an error if the maya scene is not the latest increment
    if new_path.exists() is True:
        raise RuntimeError("The current Maya scene is not the highest increment")

    # Save the file with the new name
    cmds.file(rename=new_path)
    cmds.file(save=True, force=True)

    cmds.inViewMessage(message=f"<hl>Versioned up to version '{new_number}'</hl>", pos="midCenter", fade=True, fadeStayTime=3000, clickKill=True, dragKill=True)


def save_publish():
    # Get the path to the project
    project_path = get_project_path()

    # Get a path to the current file (in Maya)
    current_file = cmds.file(query=True, sceneName=True)
    if len(current_file) == 0:
        raise FileExistsError("The current Maya scene is not in any file, please save the file, before saving an increment")

    # Check if the current file is located inside the current project
    current_file = Path(current_file)
    if current_file.is_relative_to(project_path) is False:
        # IF not, raise an error
        raise RuntimeError("The current Maya file is not located within the current project, please set the correct project")

    # Create the publish path corresponding to the current file
    publish_path_parts = list(current_file.parent.parts)
    if "edit" in publish_path_parts:
        edit_index = publish_path_parts.index("edit")
        publish_path_parts[edit_index] = "publish"
        publish_path = Path(*publish_path_parts)
    else:
        raise ValueError("The current Maya file is not in a pipeline with edit/publish folders")

    # Create the publish name
    current_scene_name = current_file.stem
    scene_extension = current_file.suffix
    name_parts = current_scene_name.split("_E_")
    if len(name_parts) != 2:
        raise NameError("The file name doesn't follow the format: 'name'_E_'number'")
    new_name = f"{name_parts[0]}_P"
    publish_path = publish_path / (new_name + scene_extension)

    # Get the selection
    sel = cmds.ls(selection=True)

    # Check if only one item is selected
    if len(sel) != 1:
        raise RuntimeError("Please select only one group for the export")
    # Check if the file path exists
    if not publish_path.parent.exists():
        raise NotADirectoryError(f"The given path '{publish_path.parent}' does not exist")
    # Check if the file name ends in _P
    if not publish_path.stem.endswith("_P"):
        raise NameError(f"The given file name is wrong, should end with '_P' as it is a publish")

    # Check if there is already a file at the given path
    if publish_path.exists():
        # Create the backup folder
        backup_path = publish_path.parent / "backup"
        if not backup_path.exists():
            backup_path.mkdir()

        new_name = publish_path.stem
        extension = publish_path.suffix
        # Query all the publish backups version numbers
        file_numbers = [int(file.stem.split("_P_")[-1]) for file in backup_path.iterdir() if file.is_file()]
        if len(file_numbers) == 0:
            publish_version_name = f"{new_name}_001" + extension
        else:
            # Pick the highest number, add 1, modify the publish name
            publish_version_name = f"{new_name}_{str(max(file_numbers)+1).zfill(3)}" + extension

        destination = backup_path / publish_version_name
        publish_path.rename(destination)

    # Export the USD file
    _export_maya_file_from_maya(export_path=publish_path, anim_data=False)
    msg = f"<hl>Model published as a Maya file</hl>"
    cmds.inViewMessage(statusMessage=msg, position="midCenter", fade=True, dragKill=True, clickKill=True)


def _export_maya_file_from_maya(export_path: Path, anim_data: bool = False):
    # Export the Maya file
    cmds.file(export_path.as_posix(), force=True, exportSelected=True, type="mayaAscii", channels=anim_data, constructionHistory=False)
