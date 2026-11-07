import time
from threading import RLock, Lock

class TTLCache:
    def __init__(self, maxsize: int, ttl: int):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.lock = Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, expire = self.cache[key]
                if expire > time.time():
                    return value
                else:
                    del self.cache[key]
            return None

    def set(self, key, value):
        with self.lock:
            if len(self.cache) >= self.maxsize:
                self.evict()
            self.cache[key] = (value, time.time() + self.ttl)

    def evict(self):
        with self.lock:
            current_time = time.time()
            to_remove = [key for key, (_, expire) in self.cache.items() if expire <= current_time]
            for key in to_remove:
                del self.cache[key]

# Example usage:
if __name__ == "__main__":
    cache = TTLCache(maxsize=10, ttl=5)
    cache.set("key1", "value1")
    time.sleep(6)
    print(cache.get("key1"))  # Output: None