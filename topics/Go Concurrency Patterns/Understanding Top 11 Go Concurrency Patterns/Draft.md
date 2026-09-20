# Understanding 11 Concurrency Patterns in Go 
Coined famously by Go co-creator Rob Pike: "Concurrency is about dealing with with lots of things at once. Parallelism is about doing lots of things at once." Because concurrency in Go is built on composable primitives - goroutines, channels, and the `select` statement, there is no single fixed number of Go concurrency patterns.

However, in professional Go development, there are 11 core, widely recognized patterns that form the foundation of almost all concurrent systems.

1. The Generator Pattern
A function that launches a goroutine to generate values asynchronously and streams them out via a read-only channel. It decouples the production of data from its consumption.

```go
func fibonacci(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		a, b := 0, 1
		for i := 0; i < n; i++ {
			out <- a
			a, b = b, a+b
		}
	}()
	return out
}
```

2. The For-Select Loop
The backbone of long-running goroutines. It continuously loops while using a `select` block to receive from or send to multiple channels, handle timeouts, or gracefully handle cancellation.

```go
func processStream(ch <-chan string, stop <-chan stuct{}) {
	for {
		select {
			case msg := <-ch:
				fmt.Println("Received:", msg)
			case <-stop:
				fmt.Println("Stopping worker...")
				return
		}
	}
}
```

3. Done Channel / Context Cancellation
Go routine leaks are a common source of memory issues. This pattern ensures parent goroutines can signal child goroutines to clean up and exit using a closed channel (or context.Context).

```go
func doWork(ctx context.Context) {
	for {
		select {
			case <-ctx.Done(): // Triggered when context is canceled or times times out
				return
			default:
				// Perform work...
				time.Sleep(100 * time.Millisecond)
		}
	}
}
```

4. Pipelines
Data is passed through a sequence of processing stages connected by channels. Each stage receives data from upstream channels, processes/transform it, and sends it downstream.

```go
// Stage 1: Generator
func generator(nums []int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums { out <- n }
		close(out)
	}
	return out
}

// Stage 2: Square
func square(in <- chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in { out <- n * n }
	}()
	return out
}
```

5. Fan-Out, Fan-In
- Fan-Out: Multiple goroutines read from the same channel to process work in parallel.

```go
func startWorkers(in <-chan int, workerCount int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup

	for i := 0; i < workerCount; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for val := range in {
				out <- val * val // Process work in parallel
			}
		}(i)
	}
	
	go func() {
		wg.Wait()
		close(out)
	}
}
```

- Fan-In: Multiple channels are multiplexed into a single channel to aggregate results.

```go
func fanIn(channels ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	output := func(c <-chan int) {
		for n := range c { out <- n }
		wg.Done()
	}

	w.Add(len(channels))
	for _, c := range channels {
		go output(c)
	}

	go func() {
		wg.Wait()
		close(out)
	}

	return out
}
```

6. Worker Pool (Bounded Parallelism)
Spawns a fixed number of worker goroutines reading from a shared job queue. This limits CPU or memory usage and avoids overwhelming external downstream APIs or database pools.

```go
func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs {
		results <- j * 2 // Simulate processing
	}
}

func main() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)
	var wg sync.WaitGroup

	// Start 3 workers
	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	for j := 1; j <= 5; j++ { jobs <- j}
	close(jobs)

	wg.Wait()
	close(results)
}
```

7. Semaphore (Counting Semaphore)
Limits the maximum number of concurrent operations (e.g., maximum 5 outgoing HTTP requests at once) using buffered channel.

```go
type Semaphore struct {
	sem chan struct{}
}

func NewSemaphore(maxReq int) *Semaphore {
	return &Semaphore{sem: make(chan struct{}, maxReq)}
}

func (s *Semaphore) Acquire() {s.sem <- struct{}{}}
func (s *Semaphore) Release() { <-s.sem }
```

8. Or-Done Channel
When consuming from a channel where the producer might not handle cancellation, this pattern wraps consumption inside a select block to ensure the reader can safely exit when the context finishes.

```go
func orDone(ctx context.Context, in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for {
			select {
				case <-ctx.Done():
					return
				case v, ok := <-in:
					if !ok { return }
					select {
						case out <- v:
						case <-ctx.Done():
							return
					}
			}
		}
	}()
	return out
}
```

9. Tee Channel
Splits a single channel stream into two identical channels (like the UNIX tee command, named after T-splitter used in plumbing) so two independent processes can evaluate the same stream of data simultaneously.

```go
func tee(done <-chan struct{}, in <-chan int) (<-chan int, <-chan int) {
	out1, out2 := make(chan int), make(chan int)
	go func() {
		defer close(out1)
		defer close(out2)
		for val := range in {
			var o1, o2 = out1, out2
			for i := 0; i < 2; i++ {
				select {
					case o1 <- val: o1 = nil
					case o2 <- val: o2 = nil
					case <-done: return
				}
			}
		}
	}()
	return out1, out2
}
```

10. Bridge Channel
Flattens a channel of channels (<-chan <- T) into a single continuous stream channel (<-chan T). This is ideal when working with pipelines that produce sequence streams.

```go
func bridge(done <-chan struct{}, chanStream <-chan <-chan int) <-chan int {
	valStream := make(chan int)
	go func() {
		defer close(valStream)
		for {
			var stream <-chan int
			select {
				case maybeStream, ok := <-chanStream:
					if !ok { return }
					stream = maybeStream
				case <-done:
					return
			}
			for val := range stream {
				select {
					case valStream <- val:
					case <-done:
						return
				}
			}
		}
	}()
	return valStream
}
```

11. Rate Limiter
Controls the rate at which operations execute over time (e.g., max 10 calls per second) using time.Ticker or token-bucket systems.

```go
func rateLimitedProcessor(requests <-chan int) {
	limiter := time.NewTicker(200 * time.Millisecond) // 5 req/sec
	defer limiter.Stop()

	for req := range requests {
		<-limiter.C // Wait for the ticker tick
		fmt.Println("Processed request:", req)
	}
}
```
