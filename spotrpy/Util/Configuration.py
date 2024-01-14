""" Configuration class """

import os
import sys
import json
import logging
import textwrap
import questionary

from rich.console import Console
from rich.logging import RichHandler


class Configuration:
    """Configuration class"""

    def __initConfig__(self):
        try:
            with open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "config.json"
                ),
                "r",
                encoding="utf-8",
            ) as file:
                self.CONFIG = json.load(file)
                self.validate_config()
        except FileNotFoundError:
            print("Config file not found!")
            create_file = str(
                input(
                    "Do you wish to create the config file and start auth process? y/n: "
                )
            )
            if create_file.lower() == "y":
                self.CONFIG = {
                    "path": os.path.dirname(os.path.realpath(__file__)),
                    "refresh_token": "",
                    "base_64": "",
                    "key": "",
                    "DEBUG": "False",
                    "API_PROCESS_DELAY": "2",
                    "ANSI_COLORS": "True",
                    "USE_ASCII_LOGO": "True",
                    "LOG_TRACK_URIS": "True",
                    "ASCII_IMAGE": "True",
                    "ASCII_IMAGE_SIZE_WIDTH": "50",
                    "ASCII_IMAGE_COLOR": "True",
                    "ASCII_IMAGE_UNICODE": "True",
                    "ASCII_IMAGE_CHARS": '@%#*+=-:.`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
                    "PRINT_DELAY_ACTIVE": "True",
                    "PRINT_DELAY": "0.01",
                }
                with open(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), "config.json"
                    ),
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(self.CONFIG, file, indent=4)
                print("Starting spotify authentication process...")
                self.__initLogging__()
                self.__initAPI__()
                self.authorise()
        self.CONFIG["ASCII_LOGO"] = textwrap.dedent(
        """
         ______     ______   ______     ______   ______    
        /\  ___\   /\  == \ /\  __ \   /\__  _\ /\  == \   
        \ \___  \  \ \  _-/ \ \ \/\ \  \/_/\ \/ \ \  __<   
         \/\_____\  \ \_\    \ \_____\    \ \_\  \ \_\ \_\ 
          \/_____/   \/_/     \/_____/     \/_/   \/_/ /_/ 
                                                        
        """
        )

    def config(self):
        """Modify config values in the terminal"""

        while True:
            configurations = [
                f"{config} - [{self.CONFIG[config]}]" for config in self.CONFIG
            ]
            config = questionary.select(
                "Select configuration | Ctrl + C to exit",
                configurations,
                erase_when_done=True,
                use_shortcuts=True,
                use_arrow_keys=True,
                use_jk_keys=False,
            ).ask()

            if config is not None:
                config = config.split(" - ")[0]
                new_config = questionary.text(
                    f"{config} - [{self.CONFIG[config]}]", erase_when_done=True
                ).ask()
                if new_config is not None and new_config != "":
                    self.CONFIG[config] = new_config
                    self.write_config()
            else:
                sys.exit()

    def write_config(self):
        """Write json data"""
        with open(
            os.path.join(self.CONFIG["path"], "config.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(self.CONFIG, file, indent=4)

    def validate_config(self):
        """Validate config.json"""
        required_keys = [
            "path",
            "refresh_token",
            "base_64",
            "key",
            "DEBUG",
            "API_PROCESS_DELAY",
            "ANSI_COLORS",
            "USE_ASCII_LOGO",
            "LOG_TRACK_URIS",
            "ASCII_IMAGE",
            "ASCII_IMAGE_SIZE_WIDTH",
            "ASCII_IMAGE_COLOR",
            "ASCII_IMAGE_UNICODE",
            "ASCII_IMAGE_CHARS",
            "PRINT_DELAY_ACTIVE",
            "PRINT_DELAY",
        ]
        config_keys = set(self.CONFIG.keys())
        if not set(required_keys).issubset(config_keys):
            missing_keys = set(required_keys) - config_keys
            self.log.error(
                "The following keys are missing in the config.json: %s",
                ", ".join(missing_keys),
            )
            self.log.info(
                "If you have an old config file, delete it and run any command"
            )
            sys.exit(1)
        else:
            return
