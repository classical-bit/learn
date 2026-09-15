# Understanding What Happens to a Backend at 3500 Requests Per Second

On a normal day, our backend handles 15 million API calls. But during big sales, traffic spikes to 3500 requests per second. E-commerce platforms need to survive 10x traffic jumps without crashing. Here is how backend systems actually work under the hood:

1. The Metrics That Matter
Daily averages don't show the real picture. We track load distribution over time:

- Active Users (DAU/MAU): Help us plan long-term needs like storage and logs.
- Peak Concurrent Users (CCU): Open connections at the exact same time. This determines if the server stays online.
- Request Per Second (RPS/QPS): Total calls reaching API gateway every second.
- Read-to-Write Ratio: How many users are viewing products versus buying them.
- Latency (Response Time): Don't look at average speeds, they hide problems. Track the slowest 5% (p95) and slowest 1% (p99) to catch hidden delays and system pauses.
Rule of Thumb: Never look at 1-hour averages. A short 10-second spike is all it takes to crash a database.

2. Where Systems Break First
Systems rarely crash because processor hits 100%. They fail at connection points:

- Database Limits: If 2000 requests hit a database that only allows 100-connections, 1900 requests get stuck waiting. Eventually, users see 504 Gateway Timeout errors.
- Database Locks: When hundreds of users try to buy the last item at the exact millisecond, it triggers `SELECT ... FOR UPDATE` or pessimistic locks. Transactions execute sequentially instead of in parallel. thread pools exhaust, and throughput drops to near zero.
- Outside Services: The backend services might handle high traffic, but if the payment provider limits at 200 QPS, the whole system backs up.

3. How to Fix it
- Edge Caching (For Reads): 90% of shopping traffic is just viewing items. Save pages on a CDN closer to the user. A 98% cache hit rate means 98 out of 100 users never even reach the main database.
- Message Queues (For Writes): Don't save heavy data instantly. Return a quick 202 Accepted and put the actual work into a background queue (like Kafka or RabbitMQ).
- Rate Limits: Block or slow down excessive traffic at the entrance using rate limiters (e.g., Token Bucket/Leaky Bucket) before it reaches the core services.

Scaling a system isn't about handling smooth everyday traffic - it's about surviving massive spikes, preventing database slowdowns, and sometimes intentionally turning off unimportant features so the core feature keeps working.
