"""
    Command interface
"""

from typing import Any, Callable, List, Union


class Command():
    """ Command """

    commands = {}

    def command(self, names: List[str], desc: str,  controller: Union[Callable[..., Any], List[Any]], options=None) -> None:
        for name in names:
            self.commands[name]=({
                "name": name, 
                "desc": desc,
                "callable": controller or [],
                "options": options or []
            }) 
