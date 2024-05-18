from ..spotr import Spotr

class Auth(Spotr):
    """ Auth """

    description = "Autheticate spotify account"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-ci','--client_id', type=str, help="Your spotify-app client-id"
        )
        parser.add_argument(
            '-cs','--client_secret', type=str, help="Your spotify-app client-secret"
        )

    def execute(self):
        self.authorise(self.args.client_id, self.args.client_secret)
