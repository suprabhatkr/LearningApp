from typing import Dict, Any, List, Tuple


DomainDef = Dict[str, Any]


_DOMAIN_TOPICS: List[DomainDef] = [
    {
        "id": "databases-persistence",
        "title": "Databases & Persistence",
        "execution_profile": "postgres",
        "topics": [
            ("001", "database_indexing", "Database Indexing (B-Trees & Hash Indexes)"),
            ("002", "connection_pooling", "Connection Pooling"),
            ("003", "transactions_acid", "Database Transactions & ACID Guarantees"),
            ("004", "isolation_levels", "Transaction Isolation Levels"),
            ("005", "n_plus_one_query", "N+1 Query Problem"),
            ("006", "migrations_versioning", "Database Migrations & Schema Versioning"),
            ("007", "optimistic_pessimistic_locking", "Optimistic vs. Pessimistic Locking"),
            ("008", "sharding_partitioning", "Database Sharding & Horizontal Partitioning"),
            ("009", "read_replicas_lag", "Read Replicas & Replication Lag"),
            ("010", "soft_hard_deletes", "Soft Deletes vs. Hard Deletes"),
        ],
    },
    {
        "id": "caching-in-memory",
        "title": "Caching & In-Memory Stores",
        "execution_profile": "redis",
        "topics": [
            ("011", "cache_aside", "Cache-Aside (Lazy Loading) Strategy"),
            ("012", "write_through_behind", "Write-Through & Write-Behind Caching"),
            ("013", "eviction_policies", "Cache Eviction Policies (LRU, LFU, FIFO)"),
            ("014", "cache_ttl", "Cache Expiration & TTL (Time To Live)"),
            ("015", "cache_stampede", "Cache Stampede (Dogpiling) & Mutex Locking"),
            ("016", "cache_penetration_bloom", "Cache Penetration & Bloom Filters"),
            ("017", "redis_hashes_sets", "Redis Data Structures: Hashes & Sets"),
            ("018", "redis_sorted_sets", "Redis Sorted Sets (ZSET) for Leaderboards"),
            ("019", "distributed_cache_sync", "Distributed Caching Synchronization"),
            ("020", "session_management_redis", "Session Management in Redis"),
        ],
    },
    {
        "id": "api-architecture",
        "title": "API Architecture & Protocols",
        "execution_profile": "api",
        "topics": [
            ("021", "rest_status_codes", "RESTful Resource Design & Status Codes"),
            ("022", "graphql_queries_mutations", "GraphQL Queries & Mutations"),
            ("023", "grpc_protobuf", "gRPC & Protocol Buffers (Protobufs)"),
            ("024", "websockets_realtime", "WebSockets for Real-Time Streaming"),
            ("025", "server_sent_events", "Server-Sent Events (SSE)"),
            ("026", "idempotency_keys", "Idempotency Keys in APIs"),
            ("027", "pagination_offset_cursor", "API Pagination: Offset vs Cursor-Based"),
            ("028", "api_versioning", "API Versioning Strategies"),
            ("029", "webhooks_signatures", "Webhooks & Retry Signatures"),
            ("030", "openapi_swagger", "OpenAPI / Swagger Schema Generation"),
        ],
    },
    {
        "id": "auth-security",
        "title": "Authentication, Authorization & Security",
        "execution_profile": "security",
        "topics": [
            ("031", "jwt_refresh", "JWT (JSON Web Tokens) & Refresh Tokens"),
            ("032", "oauth2_code_flow", "OAuth 2.0 Authorization Code Flow"),
            ("033", "rbac", "Role-Based Access Control (RBAC)"),
            ("034", "password_hashing", "Password Hashing (Argon2 / bcrypt) & Salting"),
            ("035", "rate_limiting", "Rate Limiting (Sliding Window Algorithm)"),
            ("036", "cors", "Cross-Origin Resource Sharing (CORS)"),
            ("037", "sql_injection_prevention", "SQL Injection Prevention & Prepared Statements"),
            ("038", "xss_mitigation", "Cross-Site Scripting (XSS) Mitigation & Content Sanitization"),
            ("039", "api_key_management", "API Key Management & Hashing"),
            ("040", "mutual_tls", "Mutual TLS (mTLS) Authentication"),
        ],
    },
    {
        "id": "async-queues",
        "title": "Asynchronous Processing & Message Queues",
        "execution_profile": "queue",
        "topics": [
            ("041", "message_queues", "Message Queues (RabbitMQ / Celery / Redis Queues)"),
            ("042", "pub_sub", "Publish/Subscribe (Pub/Sub) Architecture"),
            ("043", "kafka_streaming", "Event-Driven Architecture with Apache Kafka"),
            ("044", "dead_letter_queues", "Dead Letter Queues (DLQ) & Failure Handling"),
            ("045", "idempotent_consumers", "Idempotent Message Processing"),
            ("046", "task_scheduling_cron", "Task Scheduling & Cron Jobs"),
            ("047", "distributed_task_locking", "Distributed Task Locking"),
            ("048", "backpressure_flow_control", "Backpressure & Consumer Flow Control"),
            ("049", "log_compaction_retention", "Compacting & Retaining Event Logs"),
            ("050", "saga_pattern", "Saga Pattern for Distributed Transactions"),
        ],
    },
    {
        "id": "scalability-traffic",
        "title": "System Scalability & Traffic Management",
        "execution_profile": "scaling",
        "topics": [
            ("051", "load_balancing", "Load Balancing Algorithms"),
            ("052", "consistent_hashing", "Consistent Hashing"),
            ("053", "reverse_proxies", "Reverse Proxies & Edge Routers"),
            ("054", "read_write_splitting", "Database Read/Write Splitting"),
            ("055", "horizontal_vertical_scaling", "Horizontal Scaling vs. Vertical Scaling"),
            ("056", "stateful_stateless", "Stateful vs. Stateless Architecture"),
            ("057", "geo_blocking", "Dynamic IP Rate Limiting & Geo-Blocking"),
            ("058", "cdn_edge_caching", "CDN & Edge Caching"),
            ("059", "http2_http3", "HTTP/2 & HTTP/3 Multiplexing"),
            ("060", "auto_scaling_policies", "Auto-scaling Policies & Triggers"),
        ],
    },
    {
        "id": "resilience-reliability",
        "title": "Resilience, Fault Tolerance & Reliability",
        "execution_profile": "resilience",
        "topics": [
            ("061", "circuit_breaker", "Circuit Breaker Pattern"),
            ("062", "retry_backoff_jitter", "Retry Mechanisms with Exponential Backoff & Jitter"),
            ("063", "fallback_strategies", "Fallback Strategies"),
            ("064", "bulkhead_isolation", "Bulkhead Isolation Pattern"),
            ("065", "graceful_shutdown", "Graceful Shutdown & SIGTERM Handling"),
            ("066", "health_checks", "Health Checks (Liveness & Readiness Probes)"),
            ("067", "disaster_recovery", "Disaster Recovery & Database Backups"),
            ("068", "chaos_engineering", "Chaos Engineering (Fault Injection)"),
            ("069", "multi_region_failover", "High Availability & Multi-Region Failover"),
            ("070", "feature_toggles", "Rate Degradation & Feature Toggles"),
        ],
    },
    {
        "id": "observability-metrics",
        "title": "Observability, Metrics & Logging",
        "execution_profile": "observability",
        "topics": [
            ("071", "structured_logging", "Structured Logging (JSON Format)"),
            ("072", "distributed_tracing", "Distributed Tracing (OpenTelemetry)"),
            ("073", "red_use_metrics", "Metrics Aggregation (RED & USE Methods)"),
            ("074", "centralized_logs", "Centralized Log Aggregation"),
            ("075", "apm", "Application Performance Monitoring (APM)"),
            ("076", "alerting_thresholds", "Alerting Rules & Threshold Tuning"),
            ("077", "synthetic_monitoring", "Synthetic Monitoring & Canaries"),
            ("078", "pii_scrubbing", "Log Anonymization & PII Scrubbing"),
            ("079", "audit_logging", "Audit Logging & Compliance Trails"),
            ("080", "grafana_dashboards", "Real-time Dashboarding (Prometheus / Grafana)"),
        ],
    },
    {
        "id": "search-pipelines",
        "title": "Search, Indexing & Data Pipelines",
        "execution_profile": "search",
        "topics": [
            ("081", "inverted_indexes", "Inverted Indexes for Full-Text Search"),
            ("082", "tokenization_stemming", "Text Tokenization, Stemming & Lemmatization"),
            ("083", "fuzzy_search", "Fuzzy Searching & Levenshtein Distance"),
            ("084", "vector_search", "Vector Embeddings & Similarity Search"),
            ("085", "etl_pipelines", "Batch Processing (ETL Pipelines)"),
            ("086", "cdc", "Change Data Capture (CDC)"),
            ("087", "serialization_formats", "Data Serialization (JSON vs. Avro vs. MessagePack)"),
            ("088", "faceted_search", "Faceted Search & Aggregations"),
            ("089", "geospatial_queries", "Geospatial Queries & Spatial Indexing"),
            ("090", "stream_processing", "Stream Processing (Kafka Streams / Flink style)"),
        ],
    },
    {
        "id": "advanced-patterns",
        "title": "Advanced Backend Systems & Patterns",
        "execution_profile": "advanced",
        "topics": [
            ("091", "cqrs", "Command Query Responsibility Segregation (CQRS)"),
            ("092", "event_sourcing", "Event Sourcing"),
            ("093", "distributed_locking", "Distributed Locking (Redlock Algorithm)"),
            ("094", "service_mesh", "Service Mesh Architecture"),
            ("095", "canary_blue_green", "Blue-Green & Canary Deployments"),
            ("096", "bff", "BFF Pattern (Backend For Frontend)"),
            ("097", "connection_multiplexing", "Database Connection Multiplexing"),
            ("098", "zero_copy_io", "Zero-Copy I/O & High-Throughput Streaming"),
            ("099", "edge_server_includes", "Micro-Frontends Backend Integration"),
            ("100", "multi_tenant_architecture", "Multi-Tenant Database Architecture"),
        ],
    },
]


_DOMAIN_CONCEPT_TEMPLATES: Dict[str, str] = {
    "databases-persistence": "Focus on consistency, query planning, locking behavior, and throughput limits for persistent storage.",
    "caching-in-memory": "Focus on cache hit ratio, stale-data risk, eviction policy, and TTL behavior under load.",
    "api-architecture": "Focus on contract design, protocol trade-offs, payload shape, and backward compatibility.",
    "auth-security": "Focus on identity, access control boundaries, credential safety, and abuse prevention.",
    "async-queues": "Focus on async decoupling, retries, delivery guarantees, and eventual consistency.",
    "scalability-traffic": "Focus on routing efficiency, scaling strategy, and bottleneck movement during traffic spikes.",
    "resilience-reliability": "Focus on graceful degradation, fault containment, and recovery behavior.",
    "observability-metrics": "Focus on logs, traces, metrics, and alert quality to shorten mean time to resolution.",
    "search-pipelines": "Focus on indexing strategy, relevance quality, and ingestion pipeline reliability.",
    "advanced-patterns": "Focus on architecture-level patterns and trade-offs in distributed systems.",
}


_DOMAIN_PRACTICE_TEMPLATES: Dict[str, str] = {
    "databases-persistence": "Run the DB simulator with higher concurrency and compare latency/consistency output before and after tuning.",
    "caching-in-memory": "Run the cache simulator with custom TTL and request burst settings; compare hit/miss and latency.",
    "api-architecture": "Execute API flow simulation and inspect status codes, payload shape, and idempotency behavior.",
    "auth-security": "Run the security simulator and observe token lifecycle, authorization outcomes, and abuse protection metrics.",
    "async-queues": "Run queue simulation with retries and worker count changes; inspect backlog and completion timings.",
    "scalability-traffic": "Run traffic simulation with increased request volume; inspect routing and saturation metrics.",
    "resilience-reliability": "Inject a failure mode in simulation and inspect fallback, retries, and recovery timings.",
    "observability-metrics": "Run observability simulation and inspect logs, trace spans, and RED metrics output.",
    "search-pipelines": "Run search simulation with typo queries and indexing options; inspect relevance and latency.",
    "advanced-patterns": "Run architecture simulation and inspect consistency, throughput, and operational complexity metrics.",
}


_DEFAULT_CODE_BY_PROFILE: Dict[str, str] = {
    "postgres": "async def run_simulation(params):\n    # Tune pool_size / isolation / query shape\n    return await simulate_database(params)\n",
    "redis": "async def run_simulation(params):\n    # Tune ttl_seconds / cache_policy / burst_requests\n    return await simulate_cache(params)\n",
    "api": "async def run_simulation(params):\n    # Tune payload size / retry mode / pagination style\n    return await simulate_api(params)\n",
    "security": "async def run_simulation(params):\n    # Tune token_ttl / rate_limit / auth_mode\n    return await simulate_security(params)\n",
    "queue": "async def run_simulation(params):\n    # Tune worker_count / retry_count / batch_size\n    return await simulate_queue(params)\n",
    "scaling": "async def run_simulation(params):\n    # Tune request_rate / node_count / strategy\n    return await simulate_scaling(params)\n",
    "resilience": "async def run_simulation(params):\n    # Tune failure_rate / backoff / fallback_mode\n    return await simulate_resilience(params)\n",
    "observability": "async def run_simulation(params):\n    # Tune sample_rate / alert_threshold / log_level\n    return await simulate_observability(params)\n",
    "search": "async def run_simulation(params):\n    # Tune analyzer / fuzziness / index_batch_size\n    return await simulate_search(params)\n",
    "advanced": "async def run_simulation(params):\n    # Tune consistency_mode / event_volume / tenancy_model\n    return await simulate_advanced(params)\n",
}

_VOLUME1_TOPIC_DETAILS: Dict[str, Dict[str, Any]] = {
    "backend_001_database_indexing": {
        "detailed_markdown": """
### Volume 1 (Databases & Persistence) - Chapter 1
**Topic:** Database Indexing (B-Trees & Hash Indexes)

Indexes avoid full table scans by organizing lookup structures outside raw row storage.

**B-Tree**
- Balanced multi-way tree, sorted keys
- Supports exact lookup, prefix, sorting, and range scans (`BETWEEN`, `>`, `<`)
- Typical access complexity: `O(log N)`

**Hash Index**
- Bucket-based key hashing
- Excellent exact-match reads
- Does **not** support ordered/range access

#### Figure 1-1 (diagram summary)
```text
Request -> Index Layer
           |- B-Tree root -> branch -> leaf -> row pointer (ordered traversal available)
           |- Hash(key) -> bucket -> row pointer (exact match only)
```

#### Example practice
1. Run `EXPLAIN ANALYZE` on `WHERE email = 'user@site.com'` without index.
2. Add B-Tree index on `email`.
3. Re-run and compare `Sequential Scan` vs `Index Scan` and latency drop.
""",
    },
    "backend_002_connection_pooling": {
        "detailed_markdown": """
### Volume 1 (Databases & Persistence) - Chapter 1
**Topic:** Connection Pooling Architecture

Opening raw DB connections per request causes repeated TCP handshake, TLS verification, and auth cost.

Connection pools keep pre-initialized ("hot") sockets:
- request acquires pooled connection
- executes query
- returns connection

#### Figure 3-1 / pool mechanics (diagram summary)
```text
Request Threads -> Pool Queue -> Hot Connections -> DB
                 (wait when exhausted)
```

#### Interview pro-tip from volume
Large pool != always faster. Too many active connections can increase context switching and I/O thrashing.

#### Formula reference
`connections ~= (CPU cores * 2) + effective spindle count`

#### Exercise
Pool size=10, fire 50 concurrent requests. Observe queue wait time and tail latency.
""",
    },
    "backend_003_transactions_acid": {
        "detailed_markdown": """
### Volume 1 - Chapter 2
**Topic:** ACID Transactions & Concurrency Safety

**ACID**
- **Atomicity:** all-or-nothing
- **Consistency:** schema invariants preserved
- **Isolation:** concurrent txns do not leak invalid intermediate state
- **Durability:** committed writes survive crashes (WAL / persistent logs)

Use ACID to model critical operations like money transfer or inventory decrement.

#### Practical checks
1. Force failure mid-transaction and verify rollback.
2. Validate post-transaction constraints remain valid.
3. Inspect write-ahead logging behavior under abrupt restart tests.
""",
    },
    "backend_004_isolation_levels": {
        "detailed_markdown": """
### Volume 1 - Chapter 2
**Topic:** Isolation Levels

The volume maps ANSI levels to anomaly prevention:

- **Read Uncommitted** -> prevents none, dirty reads possible
- **Read Committed** -> prevents dirty reads, uses snapshot or short share locks
- **Repeatable Read** -> prevents dirty and non-repeatable reads, stable row versions per transaction
- **Serializable** -> prevents dirty/non-repeatable/phantom reads, applies SSI conflict checks

#### Practice
Run two sessions with concurrent reads/writes and compare anomalies under `READ COMMITTED` vs `SERIALIZABLE`.
""",
    },
    "backend_005_n_plus_one_query": {
        "detailed_markdown": """
### Volume 1 - Chapter 3
**Topic:** N+1 Query Problem

N+1 appears when ORM loops trigger one query for parent set + one query per child fetch.

Example from volume:
- Fetch 50 posts
- Loop and fetch each author
- Total ~51 queries (1 + 50)

Impact:
- connection pool pressure
- more roundtrips
- lower throughput

Mitigation:
- eager loading
- join prefetch
- direct SQL `JOIN`

#### Figure reference (ch3)
Pool + JOIN in one roundtrip outperforms iterative point fetches.
""",
    },
    "backend_006_migrations_versioning": {
        "detailed_markdown": """
### Volume 1 - Chapter 3
**Topic:** Migrations & Schema Versioning

Production schema changes should be incremental and version-controlled.

**Up migration** applies new shape.
**Down migration** provides rollback safety.

#### Example from volume
```sql
-- v002_add_status_to_users.sql
-- UP
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- DOWN
ALTER TABLE users DROP COLUMN status;
```

#### Practice
Run migration up/down in staging, verify old app compatibility and rollback path before production rollout.
""",
    },
    "backend_007_optimistic_pessimistic_locking": {
        "detailed_markdown": """
### Volume 1 - Chapter 2
**Topic:** Optimistic vs. Pessimistic Locking

When concurrent writers target same row:

**Pessimistic**
- lock row on read (`SELECT ... FOR UPDATE`)
- safer for high-collision paths
- can reduce concurrency

**Optimistic**
- read without lock
- write checks version/timestamp
- if version mismatch -> fail & retry
- good for read-heavy / low conflict

#### Example from volume
```sql
UPDATE products
SET stock = stock - 1, version = version + 1
WHERE id = 42 AND version = 3;
```
Fails when another writer already advanced version.
""",
    },
    "backend_008_sharding_partitioning": {
        "detailed_markdown": """
### Volume 1 - Chapter 4
**Topic:** Sharding & Horizontal Partitioning

Sharding splits large logical tables into smaller physical shards with same schema.

Routing via partition key (example): `user_id % 4`.

**Hash sharding**
- better even distribution for exact lookups
- re-sharding can require key remapping

**Range sharding**
- good range queries
- can hotspot latest partition (write skew)

#### Constraints called out in volume
- cross-shard joins are expensive
- celebrity/hot keys can overload single shard

#### Practice
Route synthetic users across 3 shards, then simulate skewed key distribution.
""",
    },
    "backend_009_read_replicas_lag": {
        "detailed_markdown": """
### Volume 1 - Chapters 4 & 5
**Topic:** Replication Structures, Read Replicas & Lag

Master-replica setup:
- master handles writes
- replicas handle reads
- replication often async

Async replication introduces lag (volume cites common ~50-200ms windows).
Result: stale reads right after write.

#### Figure 5-1 (diagram summary)
```text
Client Write -> Master ----async log shipping----> Replica A / Replica B
Client Read  -> Replica (may return old state during lag window)
```

Mitigations:
1. **Read-your-own-writes stickiness** for 1-5s after write
2. **Quorum-style consistency guardrails** (`R + W > N`) where applicable

#### Sandbox blueprint from volume
Inject ~100ms replica delay and validate sticky routing logic.
""",
    },
    "backend_010_soft_hard_deletes": {
        "detailed_markdown": """
### Volume 1 - Chapter 5
**Topic:** Soft Deletes vs. Hard Physical Purges

**Hard delete**
- physically removes rows (`DELETE FROM ...`)
- irreversible
- can affect audit/history paths

**Soft delete**
- mark row deleted (`deleted_at` timestamp / boolean)
- keep recoverability + audit trail
- queries filter out deleted rows by default

#### Example from volume
```sql
-- soft delete
UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = 12;

-- restore
UPDATE users SET deleted_at = NULL WHERE id = 12;
```

#### Volume 1 study kit highlights
- Exercise: indexing benchmark with `EXPLAIN ANALYZE`
- Exercise: pool stress test (50 concurrent vs max pool 10)
- Exercise: replica lag simulation with sticky reads
- Interview focus: B-Tree vs Hash, replication lag mitigation
""",
    },
    "backend_011_cache_aside": {
        "detailed_markdown": """
### Volume 2 (Caching & In-Memory Stores) - Chapter 1
**Topic:** Cache-Aside (Lazy Loading)

Cache-Aside flow:
1. Read cache first
2. On miss, read DB
3. Write DB result to cache
4. Return response

Benefits:
- memory used for actively queried keys only
- straightforward for read-heavy systems

Trade-offs:
- cold-start miss latency spikes
- repeated boilerplate cache-miss handling

#### Figure 2-1 (pipeline summary)
```text
Client -> App -> Cache? hit -> return
                 miss -> DB -> Cache set (TTL) -> return
```
""",
    },
    "backend_012_write_through_behind": {
        "detailed_markdown": """
### Volume 2 - Chapter 1
**Topic:** Write-Through & Write-Behind

**Write-Through**
- write cache + synchronously persist DB
- stronger consistency
- higher write latency

**Write-Behind (Write-Back)**
- acknowledge write in memory first
- flush dirty keys asynchronously in batches
- very low write latency, high throughput
- risk: cache failure before flush can lose data

#### Figure 2-1 (pipeline summary)
```text
Write-Through: App -> Cache -> DB -> ACK
Write-Behind:  App -> Cache -> ACK ; async flush -> DB
```
""",
    },
    "backend_013_eviction_policies": {
        "detailed_markdown": """
### Volume 2 - Chapter 1
**Topic:** Cache Eviction Policies

When memory is full, cache evicts keys based on policy:
- **LRU:** evict least recently used key
- **LFU:** evict least frequently used key
- **FIFO:** evict oldest inserted key

Use case guidance:
- LRU for locality-driven reads
- LFU for long-lived hot-key patterns
- FIFO only when insertion order semantics are acceptable
""",
    },
    "backend_014_cache_ttl": {
        "detailed_markdown": """
### Volume 2 - Chapter 2
**Topic:** Cache Expiration & TTL

TTL prevents permanently stale data by auto-expiring keys.

Trade-off curve:
- TTL too short -> extra DB load + more misses
- TTL too long -> stale user-facing data

Recommendation:
- use topic-specific TTLs (not uniform)
- observe miss-rate and stale-read indicators while tuning
""",
    },
    "backend_015_cache_stampede": {
        "detailed_markdown": """
### Volume 2 - Chapter 2
**Topic:** Cache Stampede (Dogpiling) & Mutex Locking

Stampede occurs when a hot key expires and many threads hit DB simultaneously.

Mitigation in volume:
- distributed mutex lock using `SETNX`
- first thread acquires lock, fetches DB, repopulates cache
- others wait/retry cache read

#### Figure 2-2 (diagram summary)
```text
Without lock: many miss threads -> DB surge
With SETNX: one winner thread -> DB; others backoff/retry cache
```

#### Blueprint (from volume)
100 concurrent requests on expired key, lock TTL=5s, retries after 50ms.
""",
    },
    "backend_016_cache_penetration_bloom": {
        "detailed_markdown": """
### Volume 2 - Chapter 2
**Topic:** Cache Penetration & Bloom Filters

Penetration: repeated requests for non-existent keys bypass cache and hammer DB.

Bloom Filter behavior:
- **bit check has 0** -> definitely not present, return 404 directly
- **all bits 1** -> probably present, continue to cache/DB path

Properties:
- no false negatives
- possible false positives

#### Figure 2-3 (diagram summary)
```text
Key -> k hash functions -> bit-array positions
Any 0 bit => reject
All 1 bits => probable member
```

Formula from volume:
`p = (1 - e^(-kn/m))^k`
""",
    },
    "backend_017_redis_hashes_sets": {
        "detailed_markdown": """
### Volume 2 - Chapter 3
**Topic:** Redis Native Data Structures: Hashes & Sets

Avoid monolithic JSON blobs when frequent partial updates are needed.

**Hashes (`HSET/HGET`)**
- field-level updates in `O(1)`
- lower serialization overhead

**Sets (`SADD/SISMEMBER`)**
- unique unordered values
- fast membership checks
- good for permissions/tags/whitelists

Volume guidance: field-targeted updates reduce payload transfer and CPU overhead.
""",
    },
    "backend_018_redis_sorted_sets": {
        "detailed_markdown": """
### Volume 2 - Chapter 3
**Topic:** Redis Sorted Sets (ZSET) for Leaderboards

ZSET stores members with numeric score and maintains sorted ranking.

Common operations:
- `ZADD` score updates (`O(log N)`)
- `ZRANGE` ordered retrieval
- `ZREVRANGE` top-N leaderboard

Typical use cases:
- gaming rank tables
- sliding-window rate limit counters
- active queue ordering
""",
    },
    "backend_019_distributed_cache_sync": {
        "detailed_markdown": """
### Volume 2 - Chapter 3
**Topic:** Distributed Cache Synchronization

Multiple app instances with local memory caches can diverge.

Coherence strategy:
1. Instance A writes DB update
2. Publish invalidation message (Redis Pub/Sub)
3. Instances B/C subscribed to channel evict affected key
4. Next read fetches fresh state

This keeps local caches convergent without centralizing every read.
""",
    },
    "backend_020_session_management_redis": {
        "detailed_markdown": """
### Volume 2 - Chapter 3 + Practice Kit
**Topic:** Shared Session Management in Redis

To scale stateless web tier horizontally, avoid per-instance RAM sessions.

Store session/token/cart state in centralized Redis so any app node can serve requests.

Benefits:
- load-balancer freedom
- node failover continuity
- easier autoscaling

#### Volume 2 hands-on blueprints (highlights)
1. Cache-aside latency gap benchmark (`~30-50ms` DB vs `<1ms` cache hit)
2. Stampede lock simulation using `SETNX`
3. Bloom filter false-positive evaluation and parameter tuning

#### Interview notes from volume
- Cache-aside invalidation race: prefer delete-on-write + short TTL/double-delete strategy
- Distinguish stampede vs penetration vs avalanche and prevention patterns
""",
    },
    "backend_021_rest_status_codes": {
        "detailed_markdown": """
### Volume 3 (API Architecture & Protocols) - Section 1
**Topic:** RESTful Resource Design & Status Codes

REST emphasizes stateless resource operations via `GET/POST/PUT/PATCH/DELETE`.

Volume 3 highlights precise status signaling:
- `200` OK
- `201` Created
- `400` Bad Request
- `401` Unauthorized
- `403` Forbidden
- `404` Not Found
- `409` Conflict
- `422` Unprocessable Entity

Error payload guidance: use RFC 7807 fields (`type`, `title`, `status`, `detail`, `instance`) for machine-readable failures.
""",
    },
    "backend_022_graphql_queries_mutations": {
        "detailed_markdown": """
### Volume 3 - Section 1
**Topic:** GraphQL Queries & Mutations

GraphQL gives field-level response control to avoid over-fetching and under-fetching.

- **Queries**: read operations
- **Mutations**: state-changing operations (sequential)

Server-side guardrails from the volume:
- resolver batching (e.g., DataLoader) to avoid N+1
- query depth limits
- query cost analysis to prevent abusive deep queries
""",
    },
    "backend_023_grpc_protobuf": {
        "detailed_markdown": """
### Volume 3 - Section 1
**Topic:** gRPC & Protobuf

gRPC uses contract-first Protobuf over HTTP/2 for high-efficiency service communication.

Strengths:
- compact binary payloads
- fast serialization/deserialization
- multiplexed streams on one connection
- header compression

RPC patterns:
1. Unary
2. Server streaming
3. Client streaming
4. Bidirectional streaming
""",
    },
    "backend_024_websockets_realtime": {
        "detailed_markdown": """
### Volume 3 - Section 2
**Topic:** WebSockets for Real-Time Streaming

WebSocket handshake:
- client sends `Upgrade: websocket`
- server returns `101 Switching Protocols`
- connection becomes persistent full-duplex TCP channel

Scaling concerns:
- long-lived stateful connections
- file descriptor pressure
- need proxy/backplane support for clustered fan-out

#### Figure 1 reference context
WebSockets are best for high-frequency bidirectional communication.
""",
    },
    "backend_025_server_sent_events": {
        "detailed_markdown": """
### Volume 3 - Section 2
**Topic:** Server-Sent Events (SSE)

SSE is unidirectional server->client streaming over standard HTTP.

Request/response headers:
- `Accept: text/event-stream`
- `Content-Type: text/event-stream`

Why it is practical:
- firewall/proxy friendly
- native browser reconnect support
- good for progress feeds and AI streaming output

Use SSE when client->server realtime channel is not required.
""",
    },
    "backend_026_idempotency_keys": {
        "detailed_markdown": """
### Volume 3 - Section 3
**Topic:** Idempotency Keys

Prevents duplicate side effects during retries (e.g., payment double-charge).

Flow:
1. Client sends `Idempotency-Key`
2. Server checks fast store (e.g., Redis)
3. If exists:
   - completed -> return cached response
   - in-progress -> return conflict/lock response
4. If absent:
   - acquire lock
   - process atomically
   - cache response with TTL
   - release lock

#### Figure 2 (diagram summary)
```text
Client -> API -> Redis key/lock -> Handler -> Persistent store -> cache response
```
""",
    },
    "backend_027_pagination_offset_cursor": {
        "detailed_markdown": """
### Volume 3 - Section 3
**Topic:** Offset vs Cursor Pagination

**Offset**
- pattern: `LIMIT X OFFSET N`
- degraded deep-page performance (`O(N)` scan/discard)
- susceptible to page drift during inserts/deletes

**Cursor**
- pattern: `WHERE id > cursor LIMIT X`
- index-friendly stable performance (`O(1)` pointer progression style)
- reduced drift risk

#### Figure 3 (summary)
Offset scans preceding rows; cursor targets next index position directly.
""",
    },
    "backend_028_api_versioning": {
        "detailed_markdown": """
### Volume 3 - Section 4
**Topic:** API Versioning Strategies

Volume compares three common patterns:

1. **Path**: `/v1/users`, `/v2/users` (explicit, cache-friendly)
2. **Query param**: `/users?version=2` (clean path, mixed cache behavior)
3. **Header**: vendor/media-type header versioning (URL purity, higher client complexity)

Key implementation need:
- translation/adaptation layer so older client contracts remain stable during internal evolution.
""",
    },
    "backend_029_webhooks_signatures": {
        "detailed_markdown": """
### Volume 3 - Section 4
**Topic:** Webhooks, Signatures & Retries

Security baseline:
- sign payload with HMAC-SHA256 (`X-Signature-256`)
- receiver recomputes signature to verify integrity/authenticity
- include timestamp window check to block replay attacks

Reliability baseline:
- retry non-2xx deliveries
- exponential backoff + jitter
- dead-letter queue for exhausted retries
""",
    },
    "backend_030_openapi_swagger": {
        "detailed_markdown": """
### Volume 3 - Section 4 + Practice Kit
**Topic:** OpenAPI / Swagger Schema Generation

OpenAPI is the machine-readable API contract.

Code-first workflow (e.g., FastAPI + Pydantic):
- endpoint models auto-generate OpenAPI JSON
- powers Swagger UI
- enables request validation and SDK generation

#### Volume 3 practical snippets covered
- lightweight WebSocket echo server
- FastAPI + Pydantic validation returning `422` for semantic validation failures

#### Comparative matrix insight
REST/GraphQL fit public web/API flexibility needs; gRPC is highly efficient for internal service-to-service calls.
""",
    },
    "backend_031_jwt_refresh": {
        "detailed_markdown": """
### Volume 4 (Authentication, Authorization & Security) - Section 1
**Topic:** Stateless JWT & Rotating Refresh Tokens

JWT access tokens are short-lived, signed credentials validated locally by services (no per-request DB dependency).

Recommended split:
- **Access token**: short TTL (e.g., ~15 min)
- **Refresh token**: long TTL, protected cookie (`HttpOnly`, `SameSite=Strict`)

Rotation rule:
Every refresh invalidates previous refresh token and issues a new pair.
If a stolen refresh token is replayed, revoke the token family and force re-authentication.

#### Figure 4.1 (summary)
PKCE + token issuance + refresh rotation sequence with replay detection.
""",
    },
    "backend_032_oauth2_code_flow": {
        "detailed_markdown": """
### Volume 4 - Section 1
**Topic:** OAuth 2.0 Authorization Code Flow with PKCE

PKCE protects public clients (SPA/mobile) that cannot safely hold client secrets.

Flow:
1. Client creates `code_verifier`
2. Client derives `code_challenge` and redirects to IdP
3. IdP authenticates user and returns authorization code
4. Client exchanges code + original verifier
5. Server verifies challenge/verifier match, then issues tokens

Security benefit:
Stolen auth codes are unusable without the original verifier.
""",
    },
    "backend_033_rbac": {
        "detailed_markdown": """
### Volume 4 - Section 1
**Topic:** Role-Based Access Control (RBAC)

RBAC maps users to roles (`Admin`, `Editor`, `Viewer`) and roles to permissions.

Gateway/API behavior:
- extract role/scope claims from JWT
- evaluate policy before handler execution
- return `403 Forbidden` on denied operation

Example:
`Viewer` attempting `/admin/delete-db` should be blocked immediately.
""",
    },
    "backend_034_password_hashing": {
        "detailed_markdown": """
### Volume 4 - Section 2
**Topic:** Password Hashing (Argon2/bcrypt) & Salting

Never store plaintext passwords.

Required controls:
- unique random salt per password
- slow, adaptive hashing function

Why:
- salts neutralize rainbow-table reuse
- cost factors/memory hardness slow brute-force and hardware-accelerated attacks

Volume guidance:
- bcrypt with calibrated work factor
- Argon2id for modern memory-hard defense profiles
""",
    },
    "backend_035_rate_limiting": {
        "detailed_markdown": """
### Volume 4 - Section 2
**Topic:** Sliding Window Rate Limiting

Fixed windows allow edge bursts; sliding windows provide tighter control.

Sliding window log pattern:
1. prune timestamps older than `(now - window)`
2. add current timestamp
3. count active entries
4. allow or return `429 Too Many Requests` + `Retry-After`

Redis model:
- sorted set keyed by principal (`user/ip`)
- timestamp score for each request

#### Figure 4.2 (summary)
Timestamp pruning + append + threshold check loop.
""",
    },
    "backend_036_cors": {
        "detailed_markdown": """
### Volume 4 - Section 2
**Topic:** Cross-Origin Resource Sharing (CORS)

CORS is browser-enforced origin policy, not backend authorization.

Preflight behavior:
- browser sends `OPTIONS`
- server returns explicit allow headers:
  - `Access-Control-Allow-Origin`
  - `Access-Control-Allow-Methods`
  - `Access-Control-Allow-Credentials` (if needed)

Guidance:
- use strict allow-list
- avoid wildcard origins when credentials are enabled
""",
    },
    "backend_037_sql_injection_prevention": {
        "detailed_markdown": """
### Volume 4 - Section 3
**Topic:** SQL Injection Prevention & Prepared Statements

SQL injection happens when untrusted input is concatenated into executable SQL text.

Mitigation:
- parameterized/prepared statements
- query template compiled separately from bound values

Result:
payload is treated as data literal, not executable SQL logic.
""",
    },
    "backend_038_xss_mitigation": {
        "detailed_markdown": """
### Volume 4 - Section 3
**Topic:** XSS Mitigation & Content Sanitization

XSS occurs when untrusted content is rendered as executable browser script.

Defenses:
- input sanitization
- output encoding/escaping
- strict CSP policy restricting script sources and inline execution

Operationally:
combine app-layer escaping with response headers to reduce client-side execution surface.
""",
    },
    "backend_039_api_key_management": {
        "detailed_markdown": """
### Volume 4 - Section 3 + Practice Blueprint
**Topic:** API Key Management & Hashing

API keys should be treated like credentials:
- generate high-entropy raw key
- store only one-way hash (e.g., SHA-256)
- verify by hashing presented key and comparing digest

Volume blueprint includes:
- secure key generation
- hashed DB storage
- constant-time digest comparison for verification flow
""",
    },
    "backend_040_mutual_tls": {
        "detailed_markdown": """
### Volume 4 - Section 3
**Topic:** Mutual TLS (mTLS) Authentication

Standard HTTPS is one-way identity check (client verifies server).
mTLS is two-way:
- client cert validated by server
- server cert validated by client

Use cases:
- internal service-to-service trust
- zero-trust microservice boundaries
- lateral movement reduction inside private networks

Interview framing from volume:
mTLS strengthens internal identity assurance beyond perimeter-only assumptions.
""",
    },
    "backend_041_message_queues": {
        "detailed_markdown": """
### Volume 5 (Queues) - Topic 41
**Message Queues (RabbitMQ/Celery/Redis)**

Use queues to decouple long-running work from request threads.
- API returns quickly (`202 Accepted`)
- workers process jobs asynchronously
- improves resilience under burst load
""",
    },
    "backend_042_pub_sub": {
        "detailed_markdown": """
### Volume 5 - Topic 42
**Publish/Subscribe Architecture**

One producer can fan-out events to many consumers.

#### Figure 5.1 (summary)
Point-to-point queue vs pub/sub topic broadcast to multiple subscribers.
""",
    },
    "backend_043_kafka_streaming": {
        "detailed_markdown": """
### Volume 5 - Topic 43
**Event-Driven Kafka Pipeline**

Kafka uses append-only partition logs with offset-based consumption.
- scalable replayable event streams
- consumer groups for parallel processing

#### Figure 5.2 (summary)
Partitioned commit-log with immutable offsets and consumer progress tracking.
""",
    },
    "backend_044_dead_letter_queues": {
        "detailed_markdown": """
### Volume 5 - Topic 44
**Dead Letter Queues (DLQ)**

Poison messages should not crash main consumer pools.
- retry with policy
- route repeatedly failing messages to DLQ
- inspect/replay after remediation
""",
    },
    "backend_045_idempotent_consumers": {
        "detailed_markdown": """
### Volume 5 - Topic 45
**Idempotent Message Processing**

Duplicate deliveries are expected in distributed systems.
- track message IDs/dedupe keys
- ensure repeated processing has same side effect as once
- critical for payments/inventory events
""",
    },
    "backend_046_task_scheduling_cron": {
        "detailed_markdown": """
### Volume 5 - Topic 46
**Distributed Scheduling & Cron**

Scheduled tasks need cluster-safe coordination.
- define deterministic triggers
- track last-success state
- prevent overlap for long jobs
""",
    },
    "backend_047_distributed_task_locking": {
        "detailed_markdown": """
### Volume 5 - Topic 47
**Distributed Task Locking (Redlock-style)**

Prevent duplicate execution across multiple workers.
- lock acquire with TTL
- renew while running
- safe release ownership checks
""",
    },
    "backend_048_backpressure_flow_control": {
        "detailed_markdown": """
### Volume 5 - Topic 48
**Backpressure & Flow Control**

Protect slow consumers from upstream overload.
- cap in-flight work
- throttle publishers
- scale workers based on lag and queue depth
""",
    },
    "backend_049_log_compaction_retention": {
        "detailed_markdown": """
### Volume 5 - Topic 49
**Log Compaction & Retention**

Balance auditability and storage cost.
- retain full stream for time window
- compact latest value per key where applicable
- use tiered storage for older segments
""",
    },
    "backend_050_saga_pattern": {
        "detailed_markdown": """
### Volume 5 - Topic 50
**Saga Pattern**

Distributed transactions use local steps + compensating actions.

#### Figure 5.3 (summary)
Saga orchestrator coordinates step execution and rollback compensation on failures.
""",
    },
    "backend_051_load_balancing": {
        "detailed_markdown": """
### Volume 6 (Scalability) - Topic 51
**Load Balancing (L4 vs L7)**

Distribute requests by algorithm:
- round robin
- least connections
- hash-based affinity

L4 is transport-aware; L7 enables route/header-level decisions.
""",
    },
    "backend_052_consistent_hashing": {
        "detailed_markdown": """
### Volume 6 - Topic 52
**Consistent Hashing**

Minimizes remapped keys when nodes change.
- use virtual nodes for balance
- avoid full key reshuffle seen in `hash(key) % N`

#### Figure 6.1 (summary)
Consistent hash ring with virtual node replication.
""",
    },
    "backend_053_reverse_proxies": {
        "detailed_markdown": """
### Volume 6 - Topic 53
**Reverse Proxies & Edge Routers**

Reverse proxy fronts services for:
- TLS termination
- routing
- buffering
- edge policy enforcement

#### Figure 6.2 context
Edge routing + backend tier dispatch.
""",
    },
    "backend_054_read_write_splitting": {
        "detailed_markdown": """
### Volume 6 - Topic 54
**Database Read/Write Splitting**

Route writes to primary, reads to replicas.
- increases read throughput
- must handle replica lag and consistency exceptions
- often implemented via routing proxy
""",
    },
    "backend_055_horizontal_vertical_scaling": {
        "detailed_markdown": """
### Volume 6 - Topic 55
**Horizontal vs Vertical Scaling**

- Vertical: bigger machine, simpler ops, hard ceiling
- Horizontal: more nodes, better elasticity, higher coordination complexity

Choose based on workload profile and failure tolerance goals.
""",
    },
    "backend_056_stateful_stateless": {
        "detailed_markdown": """
### Volume 6 - Topic 56
**Stateful vs Stateless**

Stateful nodes retain session context locally.
Stateless nodes externalize state (Redis/DB) so any node can serve any request.

Stateless design improves resilience and autoscaling behavior.
""",
    },
    "backend_057_geo_blocking": {
        "detailed_markdown": """
### Volume 6 - Topic 57
**Dynamic IP Rate Limiting & Geo-Blocking**

Apply edge defenses before app tier:
- per-IP limits
- CIDR deny lists
- geo/risk policies

Useful for DDoS mitigation and abuse throttling.
""",
    },
    "backend_058_cdn_edge_caching": {
        "detailed_markdown": """
### Volume 6 - Topic 58
**CDN & Edge Caching**

Serve static/semistatic content from PoPs near users.
- lower latency
- reduce origin load
- cache invalidation strategy is critical

#### Figure 6.3 (summary)
Edge hit path vs origin fetch latency gap.
""",
    },
    "backend_059_http2_http3": {
        "detailed_markdown": """
### Volume 6 - Topic 59
**HTTP/2 & HTTP/3 Multiplexing**

Compared to HTTP/1.1, modern transports reduce head-of-line overhead and improve concurrency.
- multiplex streams
- header compression
- faster recovery semantics (HTTP/3/QUIC)
""",
    },
    "backend_060_auto_scaling_policies": {
        "detailed_markdown": """
### Volume 6 - Topic 60
**Auto-scaling Policies**

Scale out/in based on SLO-linked signals:
- CPU/memory
- queue lag
- request latency
- error rate

Use cooldown and hysteresis to prevent scaling oscillation.
""",
    },
    "backend_061_circuit_breaker": {
        "detailed_markdown": """
### Volume 7 (Resilience) - Topic 61
**Circuit Breaker Pattern**

States:
- Closed (normal)
- Open (fail fast)
- Half-Open (probe recovery)

Prevents cascading failures during downstream outages.

#### Figure 7.1 (summary)
Closed/Open/Half-Open transition logic.
""",
    },
    "backend_062_retry_backoff_jitter": {
        "detailed_markdown": """
### Volume 7 - Topic 62
**Retry + Exponential Backoff + Jitter**

Retry transient failures safely:
- exponential delay growth
- random jitter to avoid synchronized retry storms

#### Figure 7.3 context
Jitter spreads retry waves to reduce thundering herds.
""",
    },
    "backend_063_fallback_strategies": {
        "detailed_markdown": """
### Volume 7 - Topic 63
**Fallback Strategies**

When dependencies fail, serve degraded-but-useful responses:
- stale cache
- default recommendations
- reduced feature output

Design fallbacks explicitly per endpoint criticality.
""",
    },
    "backend_064_bulkhead_isolation": {
        "detailed_markdown": """
### Volume 7 - Topic 64
**Bulkhead Isolation**

Partition resources (thread pools, queues, clients) so one failing component cannot consume all capacity.

#### Figure 7.2 (summary)
Isolated execution compartments prevent global exhaustion.
""",
    },
    "backend_065_graceful_shutdown": {
        "detailed_markdown": """
### Volume 7 - Topic 65
**Graceful Shutdown & SIGTERM**

Shutdown sequence:
1. stop accepting new traffic
2. drain in-flight requests
3. flush critical buffers/checkpoints
4. exit before orchestrator timeout
""",
    },
    "backend_066_health_checks": {
        "detailed_markdown": """
### Volume 7 - Topic 66
**Health Checks: Liveness vs Readiness**

- Liveness: process alive?
- Readiness: safe to receive traffic?

Readiness should fail when critical dependencies are unavailable; liveness should remain narrow.
""",
    },
    "backend_067_disaster_recovery": {
        "detailed_markdown": """
### Volume 7 - Topic 67
**Disaster Recovery (RPO/RTO)**

- **RPO**: acceptable data loss window
- **RTO**: acceptable recovery time

Practice backup restore drills and failover runbooks, not just backup creation.
""",
    },
    "backend_068_chaos_engineering": {
        "detailed_markdown": """
### Volume 7 - Topic 68
**Chaos Engineering**

Inject controlled failures (latency, packet loss, instance kill) to validate resilience assumptions.

Goal: discover unknown weak points before production incidents do.
""",
    },
    "backend_069_multi_region_failover": {
        "detailed_markdown": """
### Volume 7 - Topic 69
**Multi-Region High Availability & Failover**

Use active-active or active-passive topology with traffic steering.
- health-based routing
- data replication strategy
- failback plan
""",
    },
    "backend_070_feature_toggles": {
        "detailed_markdown": """
### Volume 7 - Topic 70
**Feature Toggles & Rate Degradation**

Disable expensive/non-essential features during incidents to preserve core user paths.

Feature flags provide fast operational control without redeploy.
""",
    },
    "backend_071_structured_logging": {
        "detailed_markdown": """
### Volume 8 (Observability) - Topic 71
**Structured Logging (JSON)**

Emit logs as parseable fields:
- timestamp, severity
- trace_id/span_id
- service, endpoint, tenant/user refs

Enables reliable querying and automated analytics.
""",
    },
    "backend_072_distributed_tracing": {
        "detailed_markdown": """
### Volume 8 - Topic 72
**Distributed Tracing (OpenTelemetry)**

Propagate context headers across service calls to rebuild full request path.

#### Figure 8.1 (summary)
W3C `traceparent` propagation across multi-hop service chain.
""",
    },
    "backend_073_red_use_metrics": {
        "detailed_markdown": """
### Volume 8 - Topic 73
**Metrics Aggregation: RED & USE**

- RED: Rate, Errors, Duration (service view)
- USE: Utilization, Saturation, Errors (resource view)

Track both to correlate application symptoms with infrastructure pressure.
""",
    },
    "backend_074_centralized_logs": {
        "detailed_markdown": """
### Volume 8 - Topic 74
**Centralized Log Aggregation**

Collect logs to central storage/search.
- consistent schema
- retention tiers
- correlation with traces/metrics

Precondition for incident forensics at scale.
""",
    },
    "backend_075_apm": {
        "detailed_markdown": """
### Volume 8 - Topic 75
**APM & Code Profiling**

Use profiling and transaction tracing to locate hot paths:
- slow DB queries
- heavy allocations
- lock contention
""",
    },
    "backend_076_alerting_thresholds": {
        "detailed_markdown": """
### Volume 8 - Topic 76
**Alerting Rules & Threshold Tuning**

Good alerts are actionable and low-noise.
- tie to user impact/SLOs
- use burn-rate style windows
- prevent alert fatigue via suppression and grouping
""",
    },
    "backend_077_synthetic_monitoring": {
        "detailed_markdown": """
### Volume 8 - Topic 77
**Synthetic Monitoring & Canary**

Continuous probe traffic validates user-critical flows even when real traffic is low.

Canary analysis compares new vs stable version error/latency before full rollout.
""",
    },
    "backend_078_pii_scrubbing": {
        "detailed_markdown": """
### Volume 8 - Topic 78
**PII Scrubbing**

Prevent sensitive data leakage in logs:
- redact secrets/tokens
- mask personal identifiers
- enforce logging guards in middleware
""",
    },
    "backend_079_audit_logging": {
        "detailed_markdown": """
### Volume 8 - Topic 79
**Audit Logging & Compliance Trails**

Audit logs should be tamper-evident and actor-focused:
- who did what
- when
- from where
- before/after state for critical changes
""",
    },
    "backend_080_grafana_dashboards": {
        "detailed_markdown": """
### Volume 8 - Topic 80
**Real-time Dashboarding (Prometheus/Grafana)**

Dashboards should surface:
- SLO latency/error trends
- saturation and queue lag
- deploy markers and anomaly overlays

#### Figure 8.3 context
Canary error tracking with automatic rollback thresholds.
""",
    },
    "backend_081_inverted_indexes": {
        "detailed_markdown": """
### Volume 9 (Pipelines & Search) - Topic 81
**Inverted Indexes**

Map token -> postings list(document IDs, positions) for fast full-text lookup.

#### Figure 9.1 (summary)
Document tokenization pipeline into postings structures.
""",
    },
    "backend_082_tokenization_stemming": {
        "detailed_markdown": """
### Volume 9 - Topic 82
**Tokenization, Stemming, Lemmatization**

Normalize language to improve recall:
- token split
- stopword handling
- stemming/lemma transforms

Tune analyzer pipeline per domain vocabulary.
""",
    },
    "backend_083_fuzzy_search": {
        "detailed_markdown": """
### Volume 9 - Topic 83
**Fuzzy Search & Levenshtein Distance**

Handle typos with edit-distance tolerance.
- improves UX recall
- must cap fuzziness/cost to protect latency
""",
    },
    "backend_084_vector_search": {
        "detailed_markdown": """
### Volume 9 - Topic 84
**Vector Embeddings & Similarity Search**

Semantic retrieval via dense vectors and ANN indexes.
- cosine/dot distance
- embedding quality and index tuning drive relevance
""",
    },
    "backend_085_etl_pipelines": {
        "detailed_markdown": """
### Volume 9 - Topic 85
**Batch ETL Pipelines**

Extract -> transform -> load in controlled jobs.
- schema contracts
- idempotent batch steps
- checkpointing and replay support
""",
    },
    "backend_086_cdc": {
        "detailed_markdown": """
### Volume 9 - Topic 86
**Change Data Capture (CDC)**

Capture DB log changes and propagate downstream incrementally.
- lower lag than periodic full exports
- supports near real-time indexing/materialization
""",
    },
    "backend_087_serialization_formats": {
        "detailed_markdown": """
### Volume 9 - Topic 87
**Serialization Formats (JSON/Avro/MessagePack)**

Trade-offs:
- JSON: human-readable, larger payloads
- Avro/MessagePack: compact binary, faster transport
- schema evolution strategy is key for long-lived pipelines
""",
    },
    "backend_088_faceted_search": {
        "detailed_markdown": """
### Volume 9 - Topic 88
**Faceted Search & Aggregations**

Return results + grouped counts (category/price/brand/etc.) for exploratory filtering.

Needs index fields optimized for both filtering and aggregation paths.
""",
    },
    "backend_089_geospatial_queries": {
        "detailed_markdown": """
### Volume 9 - Topic 89
**Geospatial Queries & R-Trees**

Spatial indexes accelerate "within radius/box" lookups over coordinates.

#### Figure 9.2 (summary)
R-tree hierarchy of geographic bounding rectangles.
""",
    },
    "backend_090_stream_processing": {
        "detailed_markdown": """
### Volume 9 - Topic 90
**Stream Processing (Flink/Kafka Streams style)**

Process event-time streams with windowing and stateful operators.
- late event handling
- exactly-once semantics considerations

#### Figure 9.3 context
Realtime ingestion -> stream compute -> search/index targets.
""",
    },
    "backend_091_cqrs": {
        "detailed_markdown": """
### Volume 10 (Advanced) - Topic 91
**CQRS**

Separate write model from read model.
- command path optimized for correctness/business rules
- query path optimized for low-latency reads and projections

#### Figure 10.1 context
Request separation across command/query paths.
""",
    },
    "backend_092_event_sourcing": {
        "detailed_markdown": """
### Volume 10 - Topic 92
**Event Sourcing**

Persist state changes as immutable events.
- replay to rebuild state
- supports auditability and temporal debugging
- requires projection/materialization strategy
""",
    },
    "backend_093_distributed_locking": {
        "detailed_markdown": """
### Volume 10 - Topic 93
**Distributed Locking (Redlock)**

Use lease-based locks for cross-node critical sections.
- lock ownership token
- bounded TTL + renewal
- careful failure semantics to avoid split ownership
""",
    },
    "backend_094_service_mesh": {
        "detailed_markdown": """
### Volume 10 - Topic 94
**Service Mesh (Istio/Linkerd)**

Move traffic/security/telemetry concerns to sidecar/control plane:
- mTLS between services
- retries/timeouts/policy
- distributed telemetry

#### Figure 10.2 (summary)
Sidecar proxy data-plane routing with mTLS enforcement.
""",
    },
    "backend_095_canary_blue_green": {
        "detailed_markdown": """
### Volume 10 - Topic 95
**Blue-Green & Canary Deployments**

- Blue-Green: full environment switchover
- Canary: gradual traffic shift + metric-based promotion/rollback

Use automated gates on error, latency, and saturation.
""",
    },
    "backend_096_bff": {
        "detailed_markdown": """
### Volume 10 - Topic 96
**Backend For Frontend (BFF)**

Create client-specific API facades (web/mobile/admin) to optimize payloads and interaction patterns.

Reduces client complexity and avoids one-size-fits-all endpoint bloat.
""",
    },
    "backend_097_connection_multiplexing": {
        "detailed_markdown": """
### Volume 10 - Topic 97
**Database Connection Multiplexing**

Pool/proxy layers share fewer backend DB connections across many app requests.

Benefits:
- lower connection churn
- reduced DB process overhead
- better admission control under spikes
""",
    },
    "backend_098_zero_copy_io": {
        "detailed_markdown": """
### Volume 10 - Topic 98
**Zero-Copy I/O & High-Throughput Streaming**

Reduce user-space copying by leveraging kernel-assisted transfer paths.
- lower CPU overhead
- improved throughput for large payload streaming
""",
    },
    "backend_099_edge_server_includes": {
        "detailed_markdown": """
### Volume 10 - Topic 99
**Micro-Frontends Backend Integration (Edge Includes)**

Assemble composite responses at edge/gateway from multiple backend fragments.

Requires timeout budgets, partial-failure strategy, and cache segmentation per fragment.
""",
    },
    "backend_100_multi_tenant_architecture": {
        "detailed_markdown": """
### Volume 10 - Topic 100
**Multi-Tenant Database Architecture**

Common models:
- database-per-tenant
- schema-per-tenant
- shared schema + tenant discriminator + RLS

#### Figure 10.3 (summary)
Isolated tenant DBs vs shared tables with row-level security policy enforcement.
""",
    },
}


def _build_topic(domain_id: str, domain_title: str, execution_profile: str, raw_topic: Tuple[str, str, str]) -> Dict[str, Any]:
    number, slug, title = raw_topic
    topic_id = f"backend_{number}_{slug}"
    topic = {
        "id": topic_id,
        "number": int(number),
        "title": title,
        "domain_id": domain_id,
        "domain_title": domain_title,
        "execution_profile": execution_profile,
        "concept": _DOMAIN_CONCEPT_TEMPLATES[domain_id],
        "hands_on": _DOMAIN_PRACTICE_TEMPLATES[domain_id],
        "challenge": f"Challenge: apply one realistic tuning change for '{title}' and compare before/after metrics.",
        "quick_check": [
            f"What production risk is reduced by mastering {title}?",
            "Which metric would you watch first while validating this change?",
        ],
        "default_code": _DEFAULT_CODE_BY_PROFILE[execution_profile],
    }
    topic.update(_VOLUME1_TOPIC_DETAILS.get(topic_id, {}))
    return topic


def get_backend_learning_domains() -> List[Dict[str, Any]]:
    domains: List[Dict[str, Any]] = []
    for domain in _DOMAIN_TOPICS:
        domains.append(
            {
                "id": domain["id"],
                "title": domain["title"],
                "topic_count": len(domain["topics"]),
                "topics": [
                    {
                        "id": f"backend_{number}_{slug}",
                        "number": int(number),
                        "title": title,
                    }
                    for number, slug, title in domain["topics"]
                ],
            }
        )
    return domains


def get_backend_learning_topic(topic_id: str) -> Dict[str, Any] | None:
    for domain in _DOMAIN_TOPICS:
        for raw_topic in domain["topics"]:
            candidate = f"backend_{raw_topic[0]}_{raw_topic[1]}"
            if candidate == topic_id:
                return _build_topic(domain["id"], domain["title"], domain["execution_profile"], raw_topic)
    return None
