from spotrpy.logging.Logging import Logging
from spotrpy.config.config import Config
from spotrpy.api.API import API

"""
    BaseController for bootstrapping essential functionality
"""

class BaseController(Logging, Config, API):
    """ BaseController """

    def __init__(self, args):
        self.args = args

        self.__initLogging__(args)
        self.log.debug("[green]BaseController initialized [purple]Logging")

        self.__initConfig__()
        self.log.debug("[green]BaseController initialized [purple]Config")

        self.__initAPI__()
        self.log.debug("[green]BaseController initialized [purple]API")
