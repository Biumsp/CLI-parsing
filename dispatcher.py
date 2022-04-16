import re
from pickle import load, dump

from os import listdir
from os.path import join, isdir, isfile
from command import Command
from syntax import *

from logger.logger_setup import logger


class Dispatcher:
    def __init__(self, path="", name="dispatcher"):
        if 1:
            logger.debug("Building dispatcher from scratch")
            self.commands = {}
            logger.debug(f"Building commands from {path}")
            self._build_commands(path)
            self._to_file(path, name)

    def _to_file(self, path, name):
        file = join(path, f"{name}.disp")
        with open(file, "wb") as f:
            logger.debug(f"Saving dispatcher to file {file}")
            dump(self, f)

    def _from_file(self, path):
        def load_from_file(f):
            with open(f, "rb") as f:
                logger.debug("Building dispatcher from file")
                return load(f)

        if isdir(path):
            for f in listdir(path):
                f = join(path, f)
                if isfile(f) and f.endswith(".disp"):
                    self = load_from_file(f)
                    return
            return 1

        elif isfile(path) and path.endswith(".disp"):
            self = load_from_file(path)

        else:
            return 1

    def _build_commands(self, path):
        dirs = filter(lambda x: isdir(join(path, x)),
                      (dir for dir in listdir(path)))

        for dir in dirs:
            if dir.endswith('_command'):
                logger.debug("Building command %s", dir)

                name = dir.replace('_command', '')
                cmd = Command(join(path, dir), name)
                self.commands.update({name: cmd})

    def dispatch(self, cli_input: str):
        if not cli_input:
            return 1

        if not self._is_correct_syntax(cli_input):
            logger.error("Incorrect syntax")
            return 1

        cli_input = self._parse(cli_input)
        cmd = cli_input["cmd"]

        if cmd in self.commands:
            self.commands[cmd].run(cli_input)
        else:
            logger.error(f"Command {cli_input['cmd']} not found")
            return 1

    def _is_correct_syntax(self, text: str):
        match = re.match(CORRECT_SYNTAX, text)
        return match

    def _parse(self, text: str):

        cli_input = {"cmd": "", "opts": [], "opts_with_args": [], "args": []}

        # Find the command and remove it
        match = re.search(CMD_RE, text)
        text = re.sub(CMD_RE, ' ', text)
        cli_input["cmd"] = match.group('cmd')

        # Find the options with =arg and remove them
        opts_with_args = re.findall(OPTS_WITH_ARGS_RE, text)
        for opt, i in zip(opts_with_args, range(len(opts_with_args))):
            text = re.sub(opt[0], ' ', text)
            opts_with_args[i] = (opt[1], opt[2])

        cli_input["opts_with_args"] = opts_with_args

        # Find the options and remove them
        opts = re.findall(OPTS_RE, text)
        text = re.sub(OPTS_RE, ' ', text)

        cli_input["opts"] = opts

        # Find the quoted args and remove them
        quoted_args = re.findall(QUOTED_ARGS_RE, text)
        text = re.sub(QUOTED_ARGS_RE, ' ', text)

        # Find the non-quoted args and remove them
        args = re.findall(ARGS_RE, text) + quoted_args
        cli_input["args"] = args

        return cli_input

    def log_info(self):
        print("\nDispatcher")
        for cmd in self.commands.values():
            cmd.log_info()
