class Settings:
    """
    Simple settings container.
    """

    def __init__(self, data=None):
        self._settings = data.copy() if data else {}

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def has(self, key):
        return key in self._settings

    def remove(self, key):
        self._settings.pop(key, None)

    def clear(self):
        self._settings.clear()

    def all(self):
        return self._settings
