from os import listdir
from os.path import join, isfile

from option import Option

from logger.logger_setup import logger


class Command:
    def __init__(self, path, name):
        self.name = name
        self.info = ""

        self.options = {}
        self._build_options(path)

    def _build_options(self, path):
        files = filter(lambda x: isfile(join(path, x)),
                       (file for file in listdir(path)))

        for file in files:
            if file.endswith('.option'):
                logger.debug("Building option %s", file)

                name = file.replace('.option', '')
                opt = Option(join(path, file), name)
                self.options.update({name: opt})

            elif file == f'{self.name}.info':
                logger.debug("Building info %s", file)

                with open(join(path, file), 'r') as f:
                    self.info = f.read()

    def run(self, cli_input):
        if self._check_options(cli_input):
            return 1

        self._handle(cli_input)

    def _check_options(self, cli_input):
        pass

    def _handle(self, cli_input):
        pass

    def set_handle(self, handle):
        self._handle = handle

    def log_info(self):
        info = "-"*20
        info += f"\nCommand: {self.name}"
        info += f"\n{self.info}"

        print(info)

        for opt in self.options.values():
            opt.log_info()
