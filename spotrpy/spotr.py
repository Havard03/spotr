from .Util.API import API
from .Util.ASCII import ASCII
from .Util.Helpers import Helpers
from .Util.Logging import Logging
from .Util.Configuration import Configuration

class Spotr(
    Configuration, 
    Logging, 
    API, 
    ASCII, 
    Helpers,
):
    """ Spotr """
    def __init__(self):
        super().__initLogging__()
        super().__initConfig__()
        super().__initAPI__()