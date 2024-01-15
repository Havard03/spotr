from urllib.parse import urljoin, urlencode

class Seek():
    """ Seek class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Seek',
            'description': 'Seek posistion for track (in seconds)',
            'arguments': ['Seconds (posistion)'],
            'min_args': 1,
            'max_args': 1,
        }

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.API_PLAYER = spotr.API_PLAYER

    def execute(self, progress):
        """Seek posistion for track in seconds"""
        self.request(
            "PUT",
            str(f"{urljoin(self.API_PLAYER, 'seek')}?{urlencode({'position_ms': int(progress) * 1000})}")
        )

