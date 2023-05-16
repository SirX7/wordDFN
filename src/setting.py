# Manage user settings.

import json as _json
import os as _os
import subprocess as _subp
import pyperclip as _pclp
from pathlib import Path as _Path


def setting_handler() -> dict:
    """Handle the user settings by creating and/or verifing a user setting file in the JSON format."""

    # The path starting from the cwd up to the directory that host the .json setting file
    sp: _Path = _Path("./data/usr/")

    # The absolute path of the .json setting file.
    sf: _Path = _Path("./data/usr/settings.json")

    # Define a variable to serialize to a json format.
    fileContent: dict = {"api_key": "", "handler": ""}

    if sf.exists():

        with open(sf, "r") as setting:
            usrConfig = _json.load(setting)

    else:
        _os.makedirs(sp)
        sf.touch()
        with open(sf, "w") as setting:
            _json.dump(fileContent, setting)

        print(
            "Add and API KEY in the api_key section, also chose if to handle from cli or use pyperclip."
        )
        _subp.call(["gedit", sf])

        with open(sf, "r") as setting:
            usrConfig = _json.load(setting)

    return usrConfig


if __name__ == "__main__":
    print(f"Executing from {__name__}")
