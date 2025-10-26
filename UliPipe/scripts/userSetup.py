"""userSetup for UliPipe, will be loaded at each Maya startup"""

from pathlib import Path

import maya.utils
from maya import cmds


def load_uli_shelf():
    shelf_path = Path(__file__).parent / "uli_pipe" / "assets" /"shelf_UliPipe.mel"
    SHELF_NAME = "UliPipe"
    shelf_exists = cmds.shelfLayout(SHELF_NAME, exists=True)

    if shelf_exists:
        # Delete shelf
        cmds.deleteUI(SHELF_NAME, layout=True)

    # Reinstall the shelf
    maya.mel.eval(f'loadNewShelf "{shelf_path.as_posix()}";')


# If Maya not in batch mode
if cmds.about(batch=True) is False:
    load_uli_shelf()
    # maya.utils.executeDeferred(load_shelf())
