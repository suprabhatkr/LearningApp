from typing import Dict, Any, List

SYSTEM_DESIGN_CHAPTERS: Dict[str, Any] = {
    "capacity_estimation": {
        "title": "Scale & Back-of-the-Envelope Estimation",
        "content": """
### Crucial Numbers Every Senior SDE Should Know
A senior engineer starts every design with scale. You must build concrete numbers before drawing components:
* **L1 Cache reference**: $0.5$ ns
* **L2 Cache reference**: $7$ ns
* **Main Memory (RAM) reference**: $100$ ns
* **SSD Sequential Read**: $1,000,000$ ns ($1$ ms)
* **HDD Round trip / Seek**: $10$ ms
* **Network Round Trip (Same Datacenter)**: $500,000$ ns ($0.5$ ms)
* **Network Round Trip (US to Europe)**: $150$ ms

### The Power of 2 Rules
* $2^{10} \\approx 1$ Thousand (KB)
* $2^{20} \\approx 1$ Million (MB)
* $2^{30} \\approx 1$ Billion (GB)
* $2^{40} \\approx 1$ Trillion (TB)

### Scalability Math Template
If an application handles **100 Million Daily Active Users (DAU)**:
1. **Request Rate (QPS)**:
   - Assume average user makes 60 requests/day.
   - Total requests/day = 100M * 60 = 6 Billion requests/day.
   - Average QPS = $6,000,000,000 / 86400 \\approx 70,000$ QPS.
   - Peak QPS = Average QPS * 2 = 140,000 QPS.
2. **Storage Bandwidth**:
   - Write requests = 10% of total requests = 600 Million writes/day.
   - If each write is 500 bytes: Storage/day = $600M \\times 500 \\text{ bytes} = 300 \\text{ GB/day}$.
   - Over 5 years = $300 \\text{ GB} \\times 365 \\times 5 \\approx 547 \\text{ TB}$.
""",
        "example_case": "Design a capacity estimator for Twitter scale: 300M DAU, 500M tweets/day, average media size 2MB (10% tweets contain media). Solve for storage, write bandwidth, read bandwidth, cache memory requirements (assuming 80/20 rule)."
    },
    "caching": {
        "title": "Caching Strategies & Distributed Cache Design",
        "content": """
### Caching Topology
1. **In-Memory Cache**: Application-level (e.g., local dict, Guava). Extremely fast, but not distributed or synchronized across nodes.
2. **Distributed Cache**: Centralized (e.g., Redis, Memcached). Independent scaling, shared state, but incurs a network hop ($1$-$2$ ms).

### Caching Write Policies
* **Write-through**: Cache is updated synchronously with the database.
  - *Pros*: Data consistency, cache is never stale.
  - *Cons*: High write latency since we wait for two writes.
* **Write-around**: Write goes directly to DB; cache is only populated on cache misses.
  - *Pros*: No caching overhead for data written but rarely read.
  - *Cons*: Cache miss latency on first read.
* **Write-back / Write-behind**: Data written to cache immediately, and queued to be written to DB asynchronously.
  - *Pros*: Extremely low write latency, high throughput.
  - *Cons*: Risk of data loss if cache crashes before DB write completes.

### Mitigating Common Cache Failures
* **Cache Penatration**: Requests search for keys that *never* exist in cache or DB.
  - *Solution*: Store null/empty results with short expiry, or use a **Bloom Filter** in front of the cache.
* **Cache Avalanche**: Many keys expire at the same time, leading to a massive spike in DB load.
  - *Solution*: Add a random jitter (noise) to the TTL values (e.g., $TTL \\pm \\text{random}(1, 5) \\text{ mins}$).
* **Cache Stampede (Thundering Herd)**: Hot key expires, and multiple concurrent app threads miss the cache and hit DB at the same time.
  - *Solution*: Use mutual exclusion locks (mutex) on cache misses so only one thread queries DB and updates cache, or pre-compute cache before expiry.
""",
        "example_case": "Design a Distributed Rate Limiter with sliding window counter using Redis. Explain the concurrency trade-offs between Multi/Exec Transaction, Lua scripting, and Cell Rate algorithms."
    },
    "data_consistency": {
        "title": "Databases, Partitioning & CAP/PACELC Trade-offs",
        "content": """
### CAP Theorem vs PACELC
CAP states that in a network partition (**P**), you must choose between Consistency (**C**) or Availability (**A**).
**PACELC** expands this for normal operations (when there is **no** partition):
- If there is a Partition (**P**), choose Availability (**A**) or Consistency (**C**).
- Else (**E**), trade off Latency (**L**) or Consistency (**C**).
- Examples:
  - *MongoDB*: PC/EC. During partitions, it rejects writes (Consistency). During normal operation, it prioritizes Consistency.
  - *Cassandra*: PA/EL. During partitions, it remains available (Availability). During normal operation, it yields low latency (Latency) by allowing stale reads.

### Database Indexing Internals
* **B-Trees / B+ Trees**: Optimized for block storage (read-heavy). Internal nodes store keys, leaf nodes store data/pointers. Linked leaves allow fast range queries.
* **LSM-Trees (Log-Structured Merge-Tree)**: Optimized for write-heavy workloads. Writes are written sequentially to a memory buffer (`MemTable`) and an append-only transaction log (`WAL`). MemTable is flushed to immutable disk files (`SSTables`). Background compaction merges SSTables and removes obsolete records.
""",
        "example_case": "Explain the step-by-step process of transitioning a database from single-node PostgreSQL to a sharded database cluster. Focus on routing tier, shard keys, re-sharding strategies, and cross-shard queries."
    }
}

SYSTEM_DESIGN_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "rate_limiter",
        "title": "Design a Distributed Rate Limiter",
        "scale": "Million RPS, multiple datacenters",
        "design_flow": """
### 1. Requirements & Scope
- **Functional**: Rate limit API endpoints based on user ID or IP. Return HTTP 429 (Too Many Requests).
- **Non-Functional**: High availability, extremely low latency overhead (< 2ms), accurate synchronization across app servers.

### 2. Algorithmic Choices
- **Token Bucket**: Stores tokens. Refilled at rate $R$. Easy to implement, allows bursts.
- **Leaky Bucket**: FIFO queue of requests, processed at constant rate. Smooths out traffic spikes, but can delay requests.
- **Sliding Window Log**: Stores log of request timestamps. Precise, but consumes massive memory.
- **Sliding Window Counter**: Combines request counts from current and previous windows. Low memory, highly accurate approximation.

### 3. Distributed Architecture
```
[Client] ---> [Load Balancer] ---> [API Gateway / Rate Limiter Middleware]
                                          | (Query redis for token counts)
                                          v
                                   [Redis Cluster]
```

### 4. Code & DB Implementation Details
We can write a Lua script to execute the rate limiting check in a single atomic step inside Redis. This prevents race conditions (Time of Check to Time of Use - TOCTOU) without expensive distributed locks:
```lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local clear_before = now - window
redis.call('zremrangebyscore', key, 0, clear_before)
local current_requests = redis.call('zcard', key)

if current_requests < limit then
    redis.call('zadd', key, now, now)
    redis.call('expire', key, window)
    return 1 -- Allowed
else
    return 0 -- Denied
end
```
"""
    },
    {
        "id": "netflix_video",
        "title": "Design a Video Streaming Service (Netflix scale)",
        "scale": "200M+ users, Petabytes of storage",
        "design_flow": """
### 1. System Components
- **Ingestion & Transcoding**: Videos are split into chunks, transcoded into multiple formats (MP4, WebM) and resolutions (1080p, 4K) asynchronously using MapReduce jobs.
- **CDN (Content Delivery Network)**: Cache static media chunks close to users to minimize latency.
- **Metadata DB**: Store movies, user profiles, history. Use highly available sharded PostgreSQL or Cassandra.

### 2. Architecture Diagram
```
                     +------------------------+
                     |    Web/Mobile App      |
                     +-----------+------------+
                                 |
           +---------------------+---------------------+
           |                                           |
           v (Metadata / Playback URLs)                v (Stream Video Chunks)
+--------------------+                       +--------------------+
|  API Gateway & DB  |                       |        CDN         |
+--------------------+                       +--------------------+
           |                                           ^
           v (Read/Write metadata)                     | (Pull cache misses)
+--------------------+                       +--------------------+
| PostgreSQL/Cassandra|                      |  S3 Media Storage  |
+--------------------+                       +--------------------+
```

### 3. Trade-offs & Optimizations
- **Adaptive Bitrate Streaming (ABR)**: Stream dynamically adjusts video quality based on current network bandwidth (HLS/DASH).
- **Edge Routing**: Netflix Open Connect colocates appliances directly inside Internet Service Providers (ISPs) to serve 95% of video traffic without traversing public internet backbone.
"""
    }
]
