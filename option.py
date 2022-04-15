from json import loads


class Option:
    def __init__(self, path, name):
        data = self._from_file(path)

        self._set_attr(data, 'name', required=True, default=name)
        self._set_attr(data, 'short_name')
        self._set_attr(data, 'info')
        self._set_attr(data, 'incompatible', default=[])

    def _from_file(self, path):
        with open(path, 'r') as f:
            data = loads(f.read())

    def _set_attr(self, data, attr, required=False, default=""):
        """Looks for the attribute in the data and sets it to the instance.
        If the attribute is not found, it sets the default value.
        If the attribute is required and not found, it raises an error.
        If the attribute is required and a default value is set, the two must match."""

        try:
            value = data[attr]

            if required and default:
                assert value == default, f"Attribute <{attr}> must be equal to the file name"

            setattr(self, attr, value)

        except KeyError:
            if required:
                raise KeyError(f"Option file is missing {attr}")
            else:
                setattr(self, attr, default)

    def __str__(self):
        return f"--{self.name} -{self.short_name} {self.info}"
