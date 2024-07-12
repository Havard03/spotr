import os
import sys
import json

class Config():
    """ Config """

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
            self.log.critical("Config file not found")
            create_file = str(input("Create config? y/n: "))
            if create_file.lower() == "y":
                self.CONFIG = {
                    "path": os.path.dirname(os.path.realpath(__file__)),
                    "refresh_token": "",
                    "base_64": "",
                    "key": "",
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
            else:
                sys.exit()

    def write_config(self):
        """ Write config data """

        with open(
            os.path.join(self.CONFIG["path"], "config.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(self.CONFIG, file, indent=4)

    def validate_config(self):
        """ Validate config """

        required_keys = [
            "path",
            "refresh_token",
            "base_64",
            "key",
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
            self.log.error("The following keys are missing in the config.json: %s", ", ".join(missing_keys))
            sys.exit()        
        
        return
