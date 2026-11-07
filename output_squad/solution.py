```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class CacheItem:
    def __init__(self, value, expiration_time):
        self.value = value
        self.expiration_time = expiration_time

class CacheEngine:
    def __init__(self, max_size, ttl):
        self.cache = {}
        self.ttl = ttl
        self.max_size = max_size
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.lock = threading.Lock()

    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                self.cache[key].expiration_time = time.time() + self.ttl
            else:
                if len(self.cache) >= self.max_size:
                    self.evict()
                self.cache[key] = CacheItem(value, time.time() + self.ttl)

    def get(self, key):
        with self.lock:
            if key in self.cache and self.cache[key].expiration_time > time.time():
                return self.cache[key].value
            else:
                return None

    def remove(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]

    def clear(self):
        with self.lock:
            self.cache.clear()

    def evict(self):
        with self.lock:
            keys_to_remove = [key for key, item in self.cache.items() if item.expiration_time <= time.time()]
            for key in keys_to_remove:
                del self.cache[key]

    def get_stats(self):
        with self.lock:
            return {
                'hits': 0,  # Placeholder for hit count
                'misses': 0,  # Placeholder for miss count
                'evictions': len([key for key, item in self.cache.items() if item.expiration_time <= time.time()])
            }

# Example usage
if __name__ == "__main__":
    cache = CacheEngine(max_size=100, ttl=3600)  # Cache with max 100 items and TTL of 1 hour
    cache.put('key1', 'value1')
    print(cache.get('key1'))  # Should print 'value1'
    time.sleep(3601)  # Wait for TTL to expire
    print(cache.get('key1'))  # Should print 'None'
    cache.put('key2', 'value2')
    cache.remove('key2')
    print(cache.get('key2'))  # Should print 'None'
    cache.clear()
    print(cache.get('key1'))  # Should print 'None'
```