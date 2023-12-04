# Importing necessary modules
import os
import sys
import json
import logging
import textwrap
import questionary

# Setting up logging
log = logging.getLogger()


class Configuration:
    """Configuration class responsible for handling and validating configuration settings."""

    def __init__(self):
        # Try to read and load configuration from the 'config.json' file
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
            # Handling the case when 'config.json' file is not found
            log.critical("Config file not found!")
            create_file = str(
                input(
                    "Do you wish to create the config file and start auth process? y/n: "
                )
            )
            if create_file.lower() == "y":
                # Creating a default configuration if the user agrees
                self.CONFIG = {
                    "path": os.path.dirname(os.path.realpath(__file__)),
                    "refresh_token": "",
                    "base_64": "",
                    "key": "",
                    "genius_access_token": "",
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
                    "IGNORED_FUNCTIONS": [
                        "validate_config",
                        "parse_functions",
                        "rgb_to_ansi",
                        "resize_image",
                        "image_to_ascii",
                        "image_to_ascii_color",
                        "get_item",
                        "parse_items",
                        "refresh_key",
                        "write_playlist",
                        "write_config",
                        "play",
                        "path",
                        "base_64",
                        "request",
                        "TOKEN",
                        "CONFIG",
                        "PLAYLIST",
                        "__getstate__",
                        "__class__",
                        "__delattr__",
                        "__dict__",
                        "__dir__",
                        "__doc__",
                        "__eq__",
                        "__format__",
                        "__ge__",
                        "__getattribute__",
                        "__gt__",
                        "__hash__",
                        "__init__",
                        "__init_subclass__",
                        "__le__",
                        "__lt__",
                        "__module__",
                        "__ne__",
                        "__new__",
                        "__reduce__",
                        "__reduce_ex__",
                        "__repr__",
                        "__setattr__",
                        "__sizeof__",
                        "__str__",
                        "__subclasshook__",
                        "__weakref__",
                        "authorise_spotify",
                        "authorise_genius",
                    ],
                }
                # Writing the default configuration to 'config.json'
                with open(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), "config.json"
                    ),
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(self.CONFIG, file, indent=4)
                print("Starting spotify authentication process...")
                self.authorise()

        # ASCII logo configuration
        self.CONFIG["ASCII_LOGO"] = textwrap.dedent(
            """
            ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
            ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
            ⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
            ⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
            ⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
            ⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
            ⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃
            ⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀
            ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
            ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
            ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
                                 __      
               _________  ____  / /______
              / ___/ __ \/ __ \/ __/ ___/
             (__  ) /_/ / /_/ / /_/ /    
            /____/ .___/\____/\__/_/     
                /_/                      
        """
        )

    def config(self):
        """Allows the user to modify configuration values in the terminal."""
        while True:
            configurations = [
                f"{config} - [{self.CONFIG[config]}]" for config in self.CONFIG
            ]
            # Using questionary library to display an interactive prompt
            config = questionary.select(
                "Select configuration | Ctrl + C to exit",
                configurations,
                erase_when_done=True,
                use_shortcuts=True,
                use_arrow_keys=True,
                use_jk_keys=False,
            ).ask()

            # Logic to modify the chosen configuration parameter
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
        """Writes the current configuration to 'config.json' file."""
        with open(
            os.path.join(self.CONFIG["path"], "config.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(self.CONFIG, file, indent=4)

    def validate_config(self):
        """Validates the keys present in 'config.json'."""
        required_keys = [
            "path",
            "refresh_token",
            "base_64",
            "key",
            "genius_access_token",
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
            "IGNORED_FUNCTIONS",
        ]
        config_keys = set(self.CONFIG.keys())
        if not set(required_keys).issubset(config_keys):
            missing_keys = set(required_keys) - config_keys
            # Logging error if any key is missing
            log.error(
                "The following keys are missing in the config.json: %s",
                ", ".join(missing_keys),
            )
            log.info("If you have an old config file, delete it and run any command")
            sys.exit(1)
        else:
            return
