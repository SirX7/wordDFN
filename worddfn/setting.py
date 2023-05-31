# Manage user settings.

import json as _json
import os as _os
import pyperclip as _pclp
from pathlib import Path as _Path

# import subprocess as _subp


def setting_handler() -> dict:
    """Handle the user settings by creating and/or verifing a user setting file in the JSON format."""

    # The path starting from the user home directory up to the directory that host the .json setting file
    sp: _Path = _Path.home() / _Path(".Worddfn/conf/")

    # The absolute path of the .json setting file.
    sf: _Path = sp / "setting.json"

    if sf.exists():
        with open(sf, "r") as setting:
            usrConfig = _json.load(setting)

    else:
        _os.makedirs(sp)
        sf.touch()

        # Define the user setting to serialize to a json format.
        fileContent: dict = setting_prompt()
        print("Configuring client.....")

        with open(sf, "w") as setting:
            _json.dump(fileContent, setting)

        print(f"All Done.")
        _pclp.copy("")

        # Remove the use of subprocess calling gedit not multi-platform, every thing should be handle from the cli.
        # print(
        #     "Add an API KEY in the api_key section, also chose if to handle from cli or use pyperclip."
        # )
        # _subp.call(["gedit", sf])

        with open(sf, "r") as setting:
            usrConfig = _json.load(setting)

    return usrConfig


def setting_prompt() -> dict:
    """Prompt user to add the necessary configuration when the client is run for the first time."""
    apiKey: str = ""
    handler: str = ""
    fileContent: dict = {}

    print(f"Please insert (or copy to your clipboard) a Wordnik API key:", end=" ")
    if len(_pclp.paste()) > 0:
        apiKey = _pclp.paste()
        print(f"'{apiKey}'")
    else:
        apiKey = input(f"")

    handler = input(
        f"Enter a Handler [clipboard|default] or [cli] | Press Enter for default:"
    )

    while handler != "clipboard" and handler != "cli":
        if handler == "" or handler == "default":
            handler = "clipboard"
            break
        else:
            handler = input(
                f"Must enter one of two option [clipboard] or [cli] or press enter for clipboard:"
            )
            if handler == "" or handler == "default":
                handler = "clipboard"

    fileContent = {"api_key": apiKey, "handler": handler}
    return fileContent


if __name__ == "__main__":
    print(f"Executing from {__name__}")
