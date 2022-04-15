from os import listdir
from os.path import join, isdir
from command import Command

from logger.logger_setup import logger


class Dispatcher:
    def __init__(self, path="commands"):
        self.commands = {}

    def _build_commands(self, path):
        dirs = filter(lambda x: isdir(join(path, x)),
                      (dir for dir in listdir(path)))

        for dir in dirs:
            if dir.endswith('_command'):
                name = dir.replace('_command', '')
                cmd = Command(join(path, dir), name)
                self.commands.update({name: cmd})

    def dispatch(self, args: str):
        if not args:
            return

        cmd, opts = self._parse(args)

        if cmd in self.commands:
            self.commands[cmd].run(opts)
        else:
            logger.error("Command not found: %s", cmd)

    def _parse(self, args: str):
        return "", []
