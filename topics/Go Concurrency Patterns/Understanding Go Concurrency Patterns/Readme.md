# Understanding Go Concurrency Patterns to Build Highly Available Systems

Concurrency is not parallelism. Understanding the difference changes how you design distributed systems.

Concurrency is about structure: decomposing a program into independent pieces and switching between them efficiently (like one chef managing three pots on a stove).

Parallelism is about execution: running multiple things at the exact same time (like hiring three chefs to cook on three stoves).

Concurrency gives us a clean way to structure the code so that it can run in parallel when multi-core hardware is available.

1. Communicating Sequential Processes (CSP) Over Locks:
Instead of relying on traditional threads and complex mutex locks which freaquently lead to race conditions, deadlocks, and complex lock hierarchies - Go takes a different path based on C.A.R. Hoare's CSP model:

"Don't communicate by sharing memory; share memory by communicating."

2. The 3 Primitives You Need to Know:
- Goroutine (`go fn()`): Spawns a lightweight execution thread (starts at ~2KB memory).
- Channel (`ch <- val`): Sends data across typed conduits, provides built-in synchronization.
- Select: Handles multiple channel operations concurrently (like an async `switch` statement).

Go uses goroutines that pass messages over channels. Instead of locking a variable, you pass data along channels between isolated goroutines.

# Go Concurrency Patterns:

By combining these primitive patterns, you can build powerful concurrency patterns:
- Generator: Launches a goroutine to generate values asynchronously and stream them out using a read-only channel.
- Fan-In (Multiplexing): Merging multiple input channels into a single output stream.
- For-Select Loop: The backbone of long-running goroutines for handling streams, timeouts, and gracefull cancellations.
- Timeouts: Handled cleanly in a select statement with `time.After()`.
- Graceful Shutdowns: Communicated across a quit channel.
- Request Hedging: Queryies multiple redundant services in parallel to return the fastest result.

# Building Highly Available Systems at Scale:

When you combine these patterns, complex distributed problems become suprisingly simple.

Take Replicated Requests (Hedging) to control p99 tail latency:
1. Launch requests to multiple replica nodes (e.g., Web1 and Web2) inside goroutines.
2. Use a fanIn multiplexer with select to return the fastest response.
3. Cancel or discard the remaining slower requests.

# The Result?
- Eliminates p99 spikes caused by transient network delays or GC pauses on individual servers.
- Achieves sub-millisecond resilience without writing a single mutex, state machine, or callback chain.

This breakdown is based on Rob Pike's 2012 Google I/O presentation, "Go Concurrency Patterns". (Link in comments)

What concurrency model do you prefer in production - Go's CSP channels, Erlang's Actor model, or traditional Async/Await?

#golang #backend #systemdesign #softwareengineering #concurrency #distributed-systems

Link to the full explanation: https://youtu.be/f6kdp27TYZs?si=UMY45dGLANgIhRBJ
