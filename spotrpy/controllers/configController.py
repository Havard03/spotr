import json
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController


class ConfigController(BaseController):

    def run(self):
        hidden = ['refresh_token', 'base_64', 'key']
        
        if self.args.list:
            if self.args.list == "all":
                for c in self.CONFIG:
                    print(c, " -- ", self.CONFIG[c]) if c not in hidden else ""
            if self.args.list == "secret":
                if self.confirm.ask("Are you sure you want to print sensitive tokens into terminal?"):
                    for c in self.CONFIG:
                        print(c, " -- ", self.CONFIG[c])
            
