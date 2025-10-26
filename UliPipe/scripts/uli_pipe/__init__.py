import sys

ASSETS_TYPES = ("01_character", "02_prop", "03_item", "04_enviro", "05_module", "06_fx")


def reload_module(name="uli_pipe"):
    """Reload a module and its submodules from a given module name.

    Args:
        name (str): Module name. Default value is "uli_pipe".
    """
    for module in sys.modules.copy():
        if module.startswith(name):
            del sys.modules[module]
            print(f"Reloaded module: {module}")
