
from cachetools import TTLCache

from config.config import Config


class MemoryStore:
    name = 'core'
    def __init__(self):
        self.config = Config().get_config()
        self._memory_store = TTLCache(maxsize=self.config["redis"]["maxsize"], ttl=self.config["redis"]["ttl"])

    def save_in_memory(self, key, value):
        self._memory_store[key] = value

    def get_from_memory(self, key):
        return self._memory_store.get(key)

    def delete_from_memory(self, key):
        if key in self._memory_store:
            del self._memory_store[key]
