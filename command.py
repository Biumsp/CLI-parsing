from os import listdir
from os.path import join, isfile

from option import Option


class Command:
    def __init__(self, path, name):
        self.name = name

        self.options = {}
        self._build_options(path)

    def _build_options(self, path):
        files = filter(lambda x: isfile(join(path, x)),
                       (file for file in listdir(path)))

        for file in files:
            if file.endswith('.option'):
                name = file.replace('.option', '')
                opt = Option(join(path, file), name)
                self.options.update({name: opt})

    def run(self, opts):
        pass

    def __str__(self):
        "\n".join(opt.__str__() for opt in self.options.values())
