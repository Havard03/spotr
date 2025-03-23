from spotrpy.config.config import Config
from spotrpy.api.API import API

"""
    BaseController for bootstrapping essential functionality
"""

class BaseController(API):
    """ BaseController """

    def __init__(self, args):
        super().__init__(args)
