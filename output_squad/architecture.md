### Architecture Plan for a High-Performance Thread-Safe In-Memory Cache with TTL Expiration

#### 1. Overview
The architecture for this cache system will be built using modern, scalable, and performant technologies. The system will be designed to be highly available, thread-safe, and with built-in TTL (Time To Live) expiration for keys. This architecture will utilize components such as a concurrent data structure for thread-safe operations, timers for TTL management, and a logging system for monitoring and debugging.

#### 2. Components and File Structure

##### 2.1. Core Cache Module
- **File Structure:**
  ```
  cache-engine/
  ├── src/
  │   ├── cache/
  │   │   ├── CacheEngine.java
  │   │   ├── InMemoryCache.java
  │   │   ├── CacheItem.java
  │   │   ├── CacheStats.java
  │   ├── timer/
  │   │   ├── TTLTimer.java
  │   │   ├── TimerTask.java
  │   ├── utils/
  │   │   ├── LockUtil.java
  │   ├── exception/
  │   │   ├── CacheException.java
  │   ├── logging/
  │   │   ├── CacheLogger.java
  ├── test/
  │   ├── cache/
  │   │   ├── InMemoryCacheTest.java
  │   │   ├── CacheItemTest.java
  │   ├── timer/
  │   │   ├── TTLTimerTest.java
  │   ├── utils/
  │   │   ├── LockUtilTest.java
  │   ├── exception/
  │   │   ├── CacheExceptionTest.java
  │   ├── logging/
  │   │   ├── CacheLoggerTest.java
  ├── pom.xml
  ```

##### 2.2. CacheEngine.java
- **Description:** This is the core component responsible for managing the cache operations. It interacts with the InMemoryCache and TTLTimer.
- **Methods:**
  - `put(K key, V value, long ttl):` Adds a new entry to the cache with a specified TTL.
  - `get(K key):` Retrieves a value from the cache based on the key.
  - `remove(K key):` Removes a key-value pair from the cache.
  - `clear():` Clears all entries from the cache.
  - `getCacheStats():` Returns statistics about the cache usage.

##### 2.3. InMemoryCache.java
- **Description:** This class uses a `ConcurrentHashMap` to store key-value pairs. It provides thread-safe operations for adding, retrieving, and removing entries.
- **Methods:**
  - `put(K key, V value):` Adds or updates a key-value pair.
  - `get(K key):` Retrieves a value based on the key.
  - `remove(K key):` Removes a key-value pair.
  - `containsKey(K key):` Checks if the cache contains a key.
  - `size():` Returns the number of entries in the cache.

##### 2.4. CacheItem.java
- **Description:** Represents a single entry in the cache. It contains the value, expiration time, and other metadata.
- **Fields:**
  - `value: V`
  - `expirationTime: long`
  - `ttl: long`

##### 2.5. CacheStats.java
- **Description:** Contains statistics about the cache usage, such as hit count, miss count, and eviction count.
- **Fields:**
  - `hitCount: long`
  - `missCount: long`
  - `evictionCount: long`

##### 2.6. TTLTimer.java
- **Description:** Manages the TTL expiration for cache entries. It uses `ScheduledExecutorService` to periodically check and remove expired entries.
- **Methods:**
  - `start():` Starts the timer.
  - `stop():` Stops the timer.
  - `removeExpiredEntries():` Removes entries that have expired.

##### 2.7. TimerTask.java
- **Description:** Represents a task to be executed by the `ScheduledExecutorService`. It checks for expired entries and removes them.
- **Method:**
  - `run():` Removes expired entries from the cache.

##### 2.8. LockUtil.java
- **Description:** Provides utility methods for acquiring and releasing locks. This ensures thread safety during concurrent operations.
- **Methods:**
  - `lock(K key):` Acquires a lock for a given key.
  - `unlock(K key):` Releases a lock for a given key.

##### 2.9. CacheException.java
- **Description:** Custom exception for cache-related errors.
- **Methods:**
  - `CacheException(String message):` Constructs a new exception with the specified message.

##### 2.10. CacheLogger.java
- **Description:** Provides logging functionality for the cache system. It can be configured to log different levels of messages.
- **Methods:**
  - `info(String message):` Logs an informational message.
  - `error(String message):` Logs an error message.
  - `debug(String message):` Logs a debug message.

#### 3. Testing
- Unit tests for each component to ensure they function correctly.
- Integration tests to ensure that the cache engine, cache items, and timer work together seamlessly.
- Performance tests to measure the cache's performance under load.

#### 4. Deployment
- The cache engine can be deployed as a standalone service or integrated into larger applications.
- Configuration options should be provided to customize the cache size, TTL, and logging level.

#### 5. Monitoring and Logging
- Use the `CacheLogger` to log cache operations and statistics.
- Monitor the cache's performance and log any errors or issues that arise.

By following this architectural plan, the high-performance, thread-safe in-memory cache with TTL expiration will be designed, implemented, and tested effectively.