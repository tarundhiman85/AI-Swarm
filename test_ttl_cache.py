import pytest
import time
import threading

from ttl_cache import TTLCache

def test_init():
    cache = TTLCache(maxsize=10, ttl=60)
    assert cache.maxsize == 10
    assert cache.ttl == 60
    assert cache.cache == {}
    assert cache.lock is not None

def test_get():
    cache = TTLCache(maxsize=10, ttl=1)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    time.sleep(1.5)
    assert cache.get("key1") is None

def test_set():
    cache = TTLCache(maxsize=10, ttl=60)
    cache.set("key1", "value1")
    assert "key1" in cache.cache
    value, expire = cache.cache["key1"]
    assert value == "value1"
    assert expire > time.time()

def test_evict():
    cache = TTLCache(maxsize=10, ttl=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    time.sleep(1.5)
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_evict_maxsize():
    cache = TTLCache(maxsize=2, ttl=60)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    assert len(cache.cache) == 2
    cache.set("key4", "value4")
    assert len(cache.cache) == 2

def test_lock():
    cache = TTLCache(maxsize=10, ttl=60)
    lock = threading.Lock()
    with pytest.raises(RuntimeError):
        with cache.lock:
            with lock:
                pass

def test_cache():
    cache = TTLCache(maxsize=10, ttl=60)
    cache.set("key1", "value1")
    cache2 = TTLCache(maxsize=10, ttl=60)
    assert cache.cache != cache2.cache