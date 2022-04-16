from json import loads
from unittest import defaultTestLoader

from logger.logger_setup import logger


class Option:
    def __init__(self, path, name):
        with open(path, 'r') as f:
            data = loads(f.read())

        self._set_attr(data, 'name', required=True, default=name)
        self._set_attr(data, 'short_name')
        self._set_attr(data, 'values', default={})
        self._set_attr(data, 'info')
        self._set_attr(data, 'incompatible', default=[])

    def _set_attr(self, data, attr, required=False, default=""):
        """Looks for the attribute in the data and sets it to the instance"""

        try:
            value = data[attr]

            # If the attribute is required and a default value is set, the two must match
            if required and default:
                assert value == default, f"Attribute <{attr}> must be equal to the file name"

            logger.debug(f"Setting {attr} to {value}")
            setattr(self, attr, value)

        except KeyError:
            if required:
                # If the attribute is required and not found, it raises an error
                raise KeyError(f"Option file is missing {attr}")
            else:
                # If the attribute is not found, it sets the default value
                setattr(self, attr, default)

    def log_info(self):
        info = f"\t--{self.name:9} -{self.short_name:2} : {self.info}"
        if self.values:
            for value, text in self.values.items():
                info += f"\n\t\t{value} : {text}"

        print(info)
