# Explanation
Rob Pike's 2012 Google I/O presentation, "Go Concurrency Patterns," serves as the conceptual blueprint for how go approaches concurrent progamming.

Rather than focusing merely on language syntax, the talk explains __how to reason about, structure, and design concurrent sustems__ using Go's primitives - goroutine, channels, and the `select` statement - to build reliable, high throughput software without thread locks and shared state.

1. The Foundation: Concurrency vs. Parallelism
Pike begins by dismantling a common misconception: Concurrency is not parallelism.

- __Concurrency is about structure__. It is the composition of independently executing computations. A concurrent program handles multiple tasks by breaking them into smaller, modular components that can run independently.
- __Parallelism__ is about execution of multiple things at the same instant on multiple physical CPU cores.

__The core thesis:__ Concurreny provides a way to structure your code cleanly so that it can run in parallel when multi-core hardware is available, but it remains easy to reason about even on a single core.

2. Theoretical Lineage & The Go Motto
Go's concurreny model does not rely on tradtional POSIX threads, mutexes, or shared memory locks. Instead, it is heavily inspired by C.A.R Hoare's 1978 paper __Communicating Sequential Processes (CSP), as well as earlier systems languages designed by Pike and his colleagues at Bell Labs (Newsqueak, Alef, Limbo).

The fundamental philosophy of Go concurreny is summarized in its famous motto:
> "Do not communicate by sharing memory; instead, share memory by communicating."

Rather than having multiple threads compete for access to shared variables guareded by mutexes (which leads to race conditions, deadlocks, and complex lock hierarchies), Go encourages passing data along channels between isolated, independent executing routines.

3. The Three Primitive Building Blocks
Pike demonstrates that Go achieves its concurrency model using three main language features:
- Goroutines:
  - A goroutine is an independently executing function launched by prefixing a call with `go` (e.g., ``` go search()``` ). 
  - Unlike heavy operating system threads (which consume megabytes of memory and require expensive kernel context switches), goroutines are managed by the Go runtime scheduler. They start with tiny growable stacks (a few kilobytes), making it practical to run tens of thousands - or even millions - of goroutines concurrently.
- Channels:
  - Channels are typed first-class values used to pass messages between goroutines.
  - Unbuffered channels provide both communication and synchronization: sending data (ch <- val) blocks until another goroutine is ready to receive(<-ch), ensuring both sides reach a known synchronization point without manual locks.
- The `select` Statement:
  - `select` is the control structure that makes Go channels expressively powerful. It acts like a `switch` statement for channel communications, enabling a goroutine to wait on multiple channel operations simultaneously and proceed with whichever channel is ready first.

4. Step-by-Step Evolution of Patterns
The talk progresses through a series of practical code patterns, building from basic constructs to a production-grade distributed architecture.

### Pattern 1: Generators (Function returning Channels)
Instead of starting a goroutine and having it talk to global state, a function creates a channel, launches a background worker, and returns the channel to the caller. The returned channel acts as a stream generator producing results asynchronously.

### Patern 2: Multiplexing (Fan-In)
When multiple goroutines are producing data, a `fanIn` function merges multiple input channels into a single output channel. This decouples the consumer from knowing who produced the data or how many workers are running.

### Pattern 3: Non-Blocking & Timed Communication (`select`)
Pike highlights how `select` handles edge cases in network programming:
- Timeouts: By combining `select` with `time.After(d)`, a channel operation can give up after a set duration, avoiding hanging goroutines if an upstream service fails.
- Quit Signals: A worker goroutine can listen for a signal on a `quit` channel to perform clean teardowns gracefully.

5. The Ultimate Demonstraton: Google Search Engine Architecture
To tie all these concepts together, Pike constructs a simulation of a Google Search backend. The problem statement: Given a user query, query Web, Image and Video search backends and return the unified results as fast as possible.

Pike iterates through three solutions to show how concurrency transforms software architecture:

1. Sequential Version:
- Calls `Web(query)`, then `Image(query)`, then `Video(query)` sequentially.
- Drawback: Total latency is the sum of all three queries. If one backend stalls, the whole request hangs.
2. Concurrent Version (Fan-In + Timeouts):
- Launches all three backend queries in separate goroutines.
- Gathers results into a channel and sets an overall request timeout (e.g., 90ms) using `select`.
- Improvement: Total latency drops to the time of the single slowest service, and slow backends are dropped cleanly without blocking the response.
3. Replicated Architecture (Tail Latency Elimination):
- To solve the problem of slow backends or transient network spikes, the system queries multiple redundant replicas for each search type (e.g., Web1 and Web2).
- A helper function: By combining fan-in, timeouts, and replication, the application achieves minimal latency and high resilience without ever writing a lock, callback, or state machine.

## Key Takeaway
The core thesis of the talk is that concurrency is a design tool for simlicity. By breaking a system into independent goroutines connected by channels, complex problems like asynchronous I/O, timeouts, cancellation, and server redundancy become straightforward, readable sequentic logic rather than tangled event loops or lock-heavy multithreaded code.

# The Talk: Go Concurrency Patterns - Rob Pike
Look around you. Do you see world doing one thing at a time? Or do you see a world of interacting, independently behaving pieces? That's why if you want to simulate that environment, a single sequential execution is not a very good approach and so concurrency is really a way of structuring your program to deal with the real world.

## What is concurrency?
- Concurrency is the composition of independently executing computations.
- Conurrency is a way to structure software, particularly as a way to write clean code that interacts well with the real world. It is not parallelism.

## Concurrency is not parallelism
- Concurrency is not parallelism, although it enables parallelism. If you have only one processor, your program can still be concurrent but it cannot be parallel. On the other hand, a well-written program might run efficiently in parallel on a multiprocessor. That property could be important.
- It is much nicer than dealing with the minutiae of parallelism (threads, semaphores, locks, barriers, etc.)

## What is a Goroutines
- It's an independently executing function, launched by a go statement.
- It has its own call stack, which grows and shrinks as required.
- It's very cheap. It's practical to have thousands, even hundreds of thousands of goroutines.
- It's not a thread.
- There might be only one thread in a program with thousands of goroutines.
- Instead, goroutines are multiplexed dynamically onto threads as needed to keep all the goroutines running.
- But if you think of it as a very cheap thread, you won't be far off.

## What are Channels?
A channel in Go provides a connection between two goroutines, allowing them to communicate.

```go
// Declaring and initializing
var c chan int
c = make(chan int)
// or
c := make(chan int)

// Sending on a channel
c <- 1

// Receiving from a channel
// The "arrow" indicates the direction of data flow
value = <-c
```

## Using Channels
A channel connects the main and boring goroutines so they can communicate

```go
func main() {
	c := make(chan string)
	go boring("boring!", c)
	for i := 0; i < 5; i++ {
		fmt.Printf("You say: %q\n", <-c) // Receive expression is just a value
	}
	fmt.Println("You're boring; I'm leaving.")
}

func boring(msg string, c chan string) {
	for := 0; ; i++ {
		c <- fmt.Sprintf("%s %d", msg, i) // Expression to be sent can be any suitable value.
		time.Sleep(time.Duration(rand.IntN(1e3)) * time.Millisecond)
	}
}
```

## Synchronization
- When the main function executes <-c, it will wait for a value to be sent.
- Similiarly, when the boring function executes c<-value, it waits for a receiver to be ready.
- A sender and receiver must both be ready to play their part in the communication. Otherwise we wait until they are.
- Thus channels both communicate and synchronize.

## An aside about buffered channels
- Note for experts: Go channels can also be created with a buffer.
- Buffering removes synchronization. Buffering makes them more like Erlang's mailboxes.
- Buffered channels can be important for some problems but they are more subtle to reason about.

## The Go Approach
Don't communicate by sharing memory, share memory by communicating.

## Paterns
Based on these priciples now we can do some concurrency patterns.
Don't think of object oriented patterns.

## Generators: function that returns a channel
Channels are first-class values, just like strings or integers.

```go
c := boring("boring!") // Function returning a channel.
for i ;= 0; i < 5; i++ {
	fmt.Printf("You say: %q\n", <-c)
}
fmt.Println("You're boring, I'm leaving.")

func boring(msg string) <-chan string { // Returns receive-only channel of strings
	c := make(chan string)
	go func() { // We launch the goroutine from inside the function
		for i := 0; ; i++ {
			c <- fmt.Sprintf("%s %d", msg, i)
			time.Sleep(time.Duration(rand.IntN(1e3)) * time.Millisecond)
		}
	}()
	return c // Return channel to the caller.
}
```

## Channels as a handle on a service
Our boring function returns a channel that lets us communicate with the boring service it provides.
We can have more instances of the service.

```go
func main() {
	joe := boring("Joe")
	ann := boring("Ann")
	for i := 0; i < 5; i++ {
		fmt.Println(<-joe)
		fmt.Println(<-ann)
	}
	fmt.Println("You're both boring, I'm Leaving.")
}
```

Ann is ready to deliver the value, but Joe hasn't done yet, so Ann will be blocked, to get around that by writing multiplexer:

## Multiplexing
These programs make Joe and Ann count in lockstep.
We can instead use a fan-in function to let whosoever is ready talk.

```go
func fanIn(input1, inout2 <-chan string) <-chan string {
	c := make(chan string)
	go func() { for { c <- <-input1 } }()
	go func() { for { c <- <-input2 } }()
	return c
}

func main() {
	c := fanIn(boring("Joe"), boring("Ann"))
	for i := 0; i < 10; i++ {
		fmt.Println(<-c)
	}
	fmt.Println("You're both boring, I'm leaving.")
}
```

## Restoring Sequencing
- Send a channel on a channel, making goroutine wait its turn.
- Receive all messages, then enable them again by sending on a private channel.
- First we define a message type that contains a channel for the reply.

```go
type Message struct {
	str string
	wait chan bool
}
```

Each speaker must wait for a go-ahead.

```go
for i := 0; i < 5; i++ {
	msg1 := <-c; fmt.Println(msg1.str)
	msg2 := <-c; fmt.Println(msg2.str)
	msg1.wait <-  true
	msg2.wait <-  true
}

waitForIt := make(chan bool) // Shared between all messages.

c <- Message{ fmt.Sprintf("%s: %d", msg, i), waitForIt }
time.Sleep(time.Duration(rand.IntN(1e3)) * time.Millisecond)
<-waitForIt
```

## Select
- A control structure unique to concurrency.
- The reason channels and goroutines are built into the language.
- The slect statement provides another way to handle multiple channels.
- All channels are evaluated.
- Selection blocks until one communication can proceed, which then does.
- If multiple can proceed, select chooses pseudo-randomly.
- A default clause, if present, executes immediately if no channel is ready.

```go
select {
	case v1 := <-c1:
		fmt.Printf("received %v from c1\n", v1)
	case v2 := <-c2:
		fmt.Printf("received %v from c2\n", v2)
	case c3 <-23:
		fmt.Printf("sent %v to c3\n", 23)
	default:
		fmt.Printf("no one was readyt to communicate\n")
}
```

## Fain-In using Select
Rewrite our original fanin function. Only one goroutine is needed. Old:

```go
func fanIn(input1, inout2 <-chan string) <-chan string {
	c := make(chan string)
	go func() { for { c <- <-input1 } }()
	go func() { for { c <- <-input2 } }()
	return c
}
```

Rewrite our original fanin function. Only one goroutine is needed. New:

```go
func fanIn(input1, input2 <-chan string) <-chan string {
	c := make(chan string)
	go func() {
		for {
			select {
				case s := <-input1: c <- s
				case s := <-input2: c <- s
			}
		}
	}()
	return c
}
```

We can use select to do all kind of interesting things.

## Timeout Using Select
The time.After function returns a channel that blocks for the specified duration.
After the interval, the channel delivers the current time, once.

```go
func main() {
	c := boring("Joe")
	for {
		select {
			case s := <-c:
				fmt.Println(s)
			case <-time.After(1 * time.Second):
				fmt.Println("You're too slow")
				return
		}
	}
}
```

## Timeout for Whole Conversation Using Select
Create the time once, outside the loop, to time out the entire conversation.

```go
func main() {
	c := boring("Joe")
	timeout := time.After(5 * time.Second)
	for {
		select {
			case s := <-c:
				fmt.Println(s)
			case <-timeout:
				fmt.Println("You talk too much")
				return
		}
	}
}
```

## Quit Channel
We can turn this around and tell Joe to stop when we're tired of listening to him.

```go
quit := make(chan bool)
c := boring("Joe", quit)
for i := rand.IntN(10); i >= 0i; i-- { fmt.Println(<-c) }
quit <- true
```
```go
select {
	case c <- fmt.Sprintf("%s: %d", msg, i):
		// do nothing
	case <-quit:
		return
}
```

## Receive on Quit Channel
How do we know it's finished? Wait for it to tell us it's done; receive on the quit channel

```go
quit := make(chan string)
c := boring("Joe", quit)
for i := rand.IntN(10); i >= 0; i-- { fmt.Println(<-c) }
quit <- "Bye!"
fmt.Printf("Joe says: %q\n", <-quit)
```
```go
select {
	case c <- fmt.Sprintf("%s: %d", msg, i):
		// do nothing
	case <-quit:
		cleanup()
		quit <- "See you!"
		return
}
```

## Daisy-chain

```go
func f(left, right chan int) {
	left <- 1 + <- right
}

func main() {
	const n = 100000
	leftmost := make(chan int)
	right := leftmost
	left := leftmost
	for i := 0; i < n; i++ {
		right = make(chan int)
		go f(left, right)
		left = right
	}
	go func(c chan int) { c <- 1 }(right)
	fmt.Println(<-leftmost)
}
```

## Systems software
Go was designed for writing systems software. Let's see how the concurrency features come into play.

## Example: Google Search
Q: What does Google search do?
A: Given a query, return a page of search results (and some ads).
Q: how do we get the search results?
A: Sen the query to Web seach, Image search, Youtube, Maps, News, etc., then mix the results.

How do we implement this?

## Google Search: A Fake Framework
We can simulate the search function, much as we simulated before.

```go
var (
	Web = fakeSearch("web")
	Image = fakeSearch("image")
	Video = fakeSearch("video")
)

type Search func(query string) Result

func fakeSearch(kind string) Search {
	return func(query string) Result {
		time.Sleep(time.Duration(rand.IntN(100)) * time.Millisecond)
		return Result(fmt.Sprintf("%s result for %q\n", kind, query))
	}
}
```

## Google Search: Test the Framework

```go
func main() {
	rand.Seed(time.Now().UnixNano())
	start := time.Now()
	results := Google("golang")
	elapsed := time.Since(start)
	fmt.Println(results)
	fmt.Println(elapsed)
}
```

## Google Search 1.0
The Goole function takes a query and returns a slice of Results (which are just strings).

Google invokes Web, Image, Video searches serially, appending them to the results slice.

```go
func Google(query string) (results []Result) {
	results = append(results, Web(query))
	results = append(results, Image(query))
	results = append(results, Video(query))
	return
}
```

## Google Search 2.0
Run the Web, Image, and Video searches concurrently, and wait for all results. No locks. No condition variables. No callbacks.

```go
func Google(query string) (results []Result) {
	c := make(chan Result)
	go func() { c <- Web(query) }
	go func() { c <- Image(query) }
	go func() { c <- Video(query) }

	for i := 0; i < 3; i++ {
		result := <-c
		results = append(results, result)
	}
	return
}
```

## Google Search 2.1
Don't wait for slow servers. No locks. No condition variables. No callbacks.

```go
c := make(chan Result)
go func() { c <- Web(query) }
go func() { c <- Image(query) }
go func() { c <- Video(query) }

timeout := time.After(80 * time.Millisecond)
for i := 0; i < 3; i++ {
	select {
		case result := <-c:
			results = append(results, result)
		case <-timeout:
			fmt.Println("timed out")
			return
	}
}
return
```

## Avoid timeout
Q: How do we avoid discarding results from slow servers?
A: Replicate the servers. Send requests to multiple replicas, and use the first response.

```go
func First(query string, replicas ...Search) Result {
	c := make(chan Result)
	searchReplica := func (i int) { c <- replicas[i](query) }
	for i := range replicas {
		go searchReplica(i)
	}
	return <-c
}

func main() {
	rand.Seed(time.Now().UnixNano())
	start := time.Now()
	result := First("golang", fakeSearch("replica 1"), fakeSearch("replica 2"))
	elapsed := time.Since(start)
	fmt.Println(result)
	fmt.Println(elapsed)
}
```

# Google Search 3.0
Reduce tail latency using replicated search servers.

```go
c := make(chan Result)
go func() { c <- First(query, Web1, Web2) }()
go func() { c <- First(query, Image1, Image2) }()
go func() { c <- First(query, Video1, Video2) }()
timeout := time.After(80 * time.Millisecond)
for i := 0; i < 3; i++ {
	select {
		case result := <-c:
			results = append(results, result)
		case <-timeout:
			fmt.Println("timed out")
			return
	}
}
return
```

## Summary
In just a few simple transformations we used Go's concurrecy primitives to convert a:
- Slow
- Sequential
- Failure-Sensitive
program into on that is:
- Fast
- Concurrent
- Replicated
- Robust
