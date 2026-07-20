class ConfigManager:
    def __init__(self, data=None):
        self._config = data.copy() if data else {}
        self._locked = False

    def load(self, data):
        self._config = data.copy()

    def reload(self, data):
        self.load(data)

    def clear(self):
        self._config.clear()

    def get(self, key, default=None):
        value = self._config

        for part in key.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value

    def has(self, key):
        return self.get(key) is not None

    def set(self, key, value):
        if self._locked:
            raise RuntimeError("Configuration is locked.")

        self._config[key] = value

    def all(self):
        return self._config

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def is_locked(self):
        return self._locked