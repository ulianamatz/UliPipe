from pathlib import Path

from maya import cmds, mel

from uli_pipe.vendor.Qt import QtWidgets


def export_obj():
    # Check if the current scene is within an existing asset
    current_path = Path(cmds.file(query=True, sceneName=True))
    if "04_asset" not in current_path.as_posix():
        msg = "<hl>Current scene is not part of an asset, could not export</hl>"
        cmds.inViewMessage(
            statusMessage=msg,
            position="midCenter",
            fade=True,
            dragKill=True,
            clickKill=True,
        )
        return

    # Check if something is selected and DAG node
    sel = cmds.ls(selection=True)
    filter_dag = [i for i in sel if "dagNode" in cmds.nodeType(i, inherited=True)]
    if len(filter_dag) == 0:
        msg = "<hl>Need a selection to export, nothing selected</hl>"
        cmds.inViewMessage(
            statusMessage=msg,
            position="midCenter",
            fade=True,
            dragKill=True,
            clickKill=True,
        )
        return

    # Get export path
    new_path = Path(current_path.as_posix().split("maya")[0])
    folder_path = new_path / "sculpt" / "zbrush" / "input"
    export_path = Path(QtWidgets.QFileDialog.getSaveFileName(dir=folder_path.as_posix(), filter="OBJ Files (*.obj)")[0])  # fmt: skip
    if export_path != Path("."):
        # Export
        cmds.select(filter_dag)
        if not cmds.pluginInfo("objExport", query=True, loaded=True):
            cmds.loadPlugin("objExport")
        mel.eval(
            f'file -force -options "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1" -type "OBJexport" -pr -es "{export_path.as_posix()}";'
        )
        msg = f"<hl>Export successful to '{export_path.as_posix()}'</hl>"
        cmds.inViewMessage(
            statusMessage=msg,
            position="midCenter",
            fade=True,
            dragKill=True,
            clickKill=True,
        )


def import_obj():
    # Check if the current scene is within an existing asset
    current_path = Path(cmds.file(query=True, sceneName=True))
    if "04_asset" not in current_path.as_posix():
        msg = "<hl>Current scene is not part of an asset, could not import</hl>"
        cmds.inViewMessage(
            statusMessage=msg,
            position="midCenter",
            fade=True,
            dragKill=True,
            clickKill=True,
        )
        return

    # Get import path
    new_path = Path(current_path.as_posix().split("maya")[0])
    folder_path = new_path / "sculpt" / "zbrush" / "output"
    import_path = Path(QtWidgets.QFileDialog.getOpenFileName(dir=folder_path.as_posix(), filter="Geo Files (*.obj *.fbx)")[0])  # fmt: skip
    if import_path != Path("."):
        # Import
        cmds.file(import_path.as_posix(), i=True)
