# Understanding E-Commerce Traffic Scale
On an average day we handle 15 million API calls, but during sale windows it peaks at 3,500 requests per second. In software engineering, scaling isn't just about throwing bigger machines at a problem (vertical scaling). It's about smart architecture. Managing high-growth e-commerce platforms and headless commerce, the baseline traffic sits around mid-tier enterprise level, but the systems are specifically stress-tested for 10x spikes during peak flash sales and holiday events.

1. Capturing Metrics
Metrics are captured across every tier of tech stack:
- Client-Side: Google Core Web Vitals (LCP, FID, CLS), JS crash rates, DOM rendering time, client network latency via JS snippets injected into pages or SDKs inside iOS/Android apps. 
- API Gateway: Requests Per Second (RPS), HTTP error rates (4xx / 5xx), latency distribution (p50, p95, p99), payload sizes via reverse proxies and gateway nodes (e.g., NGINX or AWS ALB).
- Backend Application: Orders processed per minute, active cart checkout count, payment gateway drop-off rates, Garbage collection pause times, thread pool utilization, heap memory usage, active event-loop latency via SDKs or instrumentaion libraries (e.g., OpenTelemetry) implemented directly into the code.
- Database & Caching: Connection pool utilization, active transaction locks, cache hit/miss ratios, slow query durations, IOPS via state tables (e.g., PSQL pg_stat_activity, Redis Exporter)
- Infrastructure: CPU load averages, RAM allocation, network I/O throughput, dist write queues, container pod restarts via daemon processes running on host or container nodes (e.g., Prometheus Node Exporter, Kubernetes cAdvisor).
- CDN: Cache hit ratio at the edge, bandwidth utilization, geographical latency, rate limiting triggers, SSL handshakes per second via metric streams from edge providers (e.g., Cloudflare, AWS CloudFront).

Once generated these time-stamped telemetry are exported to a central Time-Series Database (TSDB) for visualization and alerting.

In production, we don't care about "how many people visited today", we care about the load distribution over time (Throughput Profiles):

- Daily / Monthly Active Users (DAU/MAU): The baseline, it helps with long-term capacity planning like storage, logging budgets, etc.
- Peak Concurrent Users (CCU): The number of open TCP/WebSocket connections or active user sessions occuring at the exact same second. This is the metric that determines if the server stays up.
- Requests Per Second (RPS/QPS): The total volume of HTTP calls reaching the API gateway every second.
- Read-to-Write Ratio: How many requests fetch data versus how many mutate data. It is typicall 90:10 or 95:5 in e-commerce.
Note: Measure metrics at 1-second or 5-second intervals, not 1-hour average as it hides the 10-second traffic spike that takes the service offline.

Latency SLA Tracking:
- Track p95, p99, and p99.9 latencies rather than p50. Looking only at average response time hides the fact that some users are experiencing severe delays.

When measuring load for high-throughput or flash-sale systems, evaluate Peak CCU, sustained RPS vs Burst RPS, Read-to-Write ratio and payload sizes - a 35k RPS spike on a 2KB GraphQL query has vastly different network I/O demands than on a 2MB catalog response.

2. System Constraints
When traffic spikes by 10x, where does the system break first. It rarely fails because CPU usage reaches 100%. It fails at boundaries and integration points because of resource contention and bottlenecks.

A. Database Connection Limits (Thread Starvation)
The backend app connects to the database using a connection pool (e.g., maximum 100 open connections)
- If 2000 API requests arrive simultaneously without connection pooling proxies (e.g., PgBouncer) and all attempt to query the database at once, 100 requests acquire a connection while 1900 wait in queue inside app runtimes
- Once the request timeout limit (e.g., 5 seconds is exceeded), those 1900 requests fail with 504 Gateway Timeout

Database Write Locks (Hotspotting)
- 500 users targeting to purchase the last unit of an item at the same millisecond create heavy row locking (SELECT ... FOR UPDATE or pessimistic locks)
- It forces all 500 transactions to run sequentially, not in parallel. The database thread pool exhausts, causing the throughput to drop to near zero while CPU utilization hits 100%.

Third-Party API Rate Limits (Circuit Tripping)
- Third-Party integrations (payment gateways, ERP/OMS inventory synchronization, tax computation engines) often carry low rate limits (e.g., 100-200 QPS). Unthrottled calls to external services during a surge will trigger HTTP 429 Too Many requests or hard timeouts, cascading failures into the primary application.

3. Optimizations
To sustain high load, separate reads from writes and shield the database
- CDN Caching (Protect the Reads, Sub-50ms p99 response time)
Since 90% of traffic consists of read operations (browing product listings, viewing descriptions), never let those request reach your primary database. A 95%+ Cache Hit Ratio means 95 out of 100 requests never hit your main backend.
CDN serve static assets, images, and pre-rendered pages from edge locations physically close to the user. Cache Control Headers & Invalidation use Stale-While-Revalidate or HTTP Caching (s-maxage) to serve cached catalog data. Use event-driven webhooks to invalidate cache entries when price or inventory changed.

- Decouple Heavy Writes with Message Queues (Protect the Writes, High throughput order ingestion)
When a user places an order, don't write everything to the primary DB synchronously. Return 202 Accepted and dump the payload into an asynchronous message queue (e.g., Kafka / RabbitMQ) to process payment, send email confirmations, and update inventory in the background.

Architectural patterns to consider:
A. Command Query Responsibility Segregation (CQRS): Separate the read model (optimized search indices in Elasictsearch or Redis) from the write model (relational DB). Changes on the write side asynchronously propagate to the read side via event streams or Change Data Capture (CDC) tools (e.g., Debezium), resulting in eventual consistency.
B. Transactional Outbox Pattern: Gurantee At-Least-Once delivery, ensures that a database update and a corresponding event publication are atomic (they either both succeed or both fail) without using slow, complex distributed transactions like Two-Phase Commit (2PC). Eliminating the Dual-Write problem, instead of writing to a database and directly sending a message to a broker (where a network failure after step 1 leaves the system inconsistent), everything is kept inside a single local database transaction. The application writes its updates and writes an event payload to an outbox_events table (The Outbox Table) within same ACID transaction. When database commits, it appends the changes to its internal Write-Ahead-Log (WAL), A CDC engine reads the WAL directly in real time and streams the outbox events straigh to the message broker.

- Dynamic Rate Limiting & Capacity Management:
Protect the backend systems from traffic spikes, resource abuse, and brute-force attacks using:

A. Token Bucket / Leaky Bucket Algorithms:
Token Bucket: Imagine a bucket that fills with tokens at a constant rate. Each request must consume a token to pass through. If the buck has tokens, requests pass immediately - allowing breif burst of traffic up to the bucket's capacity. Once empty, further requests are blocked until token refill.
Leaky Bucket: Imagine a bucket with a small hole in the bottom. Incoming requests are added to a queue (the bucket) and leak out to processing at a strictly constant rate, regradless of how fast they enter. Any requests arriving when the queue is full are immediately rejected. This smooths out the traffic spikes into a continuous flow.
Gatekeeping at the API Gateway Layer: Instead of letting every backend microservice handle its own traffic control, rate limiting is placed at the API Gateway.
Strict Per-IP and Per-User-Session Limits
You track limits using distinct keys depending on authentication state:
Per-IP Limits: Tracks authenticated traffic based on the client's public IP address. Protects public endpoints (like /login or /register) from scraping and brute-force attacks.
Per-User-Session Limits: Tracks authenticated traffic using a unique identifier (like a User ID or JWT session claim). Prevents a single logged-in user from hogging system resources, even if they switch IP addresses or use multiple devices.
Redis-Based Distributed State
Because API Gateways are typically deployed as multiple stateless nodes behind a load balancer, local in-memory counters won't work consistently
Redis serves as a fast, centralized, in-memory data store shared by all API Gateway nodes.
It guarantees that a request arriving at Gateway Node A updates the same rate-limit state checked by Gateway Node B.
Sliding Window Counters
Unlike simple Fixed Window counters (which suffer from "boundary spikes" - where a client can send double the limit at the edge of a reset window), Sliding Window Counters calculate limits using a moving time frame (e.g., "the last 60 seconds rolling").
Redis efficiently handles this using a combination of hashes, atomic operations, or sorted sets (ZAA / ZREMRANGEBYSCORE) or lightweigh scripts to track timestamps accurately without heavy memory usage.

Enforce strict per-IP and per-user-session rate limits at API Gateway layer using Redis-backed sliding window conters.
This can return a clean HTTP 429 or puts incoming users into a managed witing line rather than allowing the database to crash for everyone:

B. Load Shedding & Graceful Degradation
When CPU/memory thresholds exceed safe operating limits, shed low-priority non-critical requests (e.g., personalization metrics, recommendations) with fallback defaults to preserve capacity for core checkout paths.

C. Circuit Breakers (e.g., Resilience4j / Envoy Filters): Automatically wrap downstream external calls in circuit breakers. If latency spikes or error rates exceed 5%, trip the circuit immediately to return fallback responses without blocking app threads.


Reference :-

Metrics:
DAU: 150K - 250K
Peak DAU: 800K
MAU: 3.5M - 4.5M
CCU: 3K - 5K
Peak CCU: 35K
RPD: 15M - 20M
Peak RPD: 45M
RPS: 250
Peak RPS: 3.5K
