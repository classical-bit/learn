# Advanced Go Concurrency Patterns - Sameer Ajmani
## Go Supports Concurrency
- In the language and runtime, not a library.
- This changes how you structure your programs.

# Goroutines and Channels
Goroutines are independently executing functions in the same address space.

```go
go f()
go g(1, 2)
```

Channels are typed values that allow goroutines to synchronize and exchange information.

```go
c := make(chan int)
go func() { c <- 3 }()
n := <- c
```

## Example: ping-pong

```go
type Ball struct{ hits int }

func main() {
	table := make(chan *Ball)
	go player("ping", table)
	go player("pong", table)

	table <- new(Ball) // game on; toss the Ball
	time.Sleep(1 * time.Second)
	<-table // game over; grab the Ball
}

func player(name string, table chan *Ball) {
	for {
		ball := <-table
		ball.hits++
		fmt.Println(name, ball.hits)
		time.Sleep(100 * time.Millisecond)
		table <- ball
	}
}
```

## Deadlock detection

```go
type Ball struct{ hits int }

func main() {
	table := make(chan *Ball)
	go player("ping", table)
	go player("pong", table)

	// table <- new(Ball) // game on; toss the Ball
	time.Sleep(1 * time.Second)
	<-table // game over; grab the Ball
}

func player(name string, table chan *Ball) {
	for {
		ball := <-table
		ball.hits++
		fmt.Println(name, ball.hits)
		time.Sleep(100 * time.Millisecond)
		table <- ball
	}
}
```

Throws - Fatal error all goroutines are asleep - deadlock!

## Panic Dumps the Stacks

```go
type Ball struct{ hits int }

func main() {
	table := make(chan *Ball)
	go player("ping", table)
	go player("pong", table)

	table <- new(Ball) // game on; toss the Ball
	time.Sleep(1 * time.Second)
	<-table // game over; grab the Ball

	panic("show me the stacks")
}

func player(name string, table chan *Ball) {
	for {
		ball := <-table
		ball.hits++
		fmt.Println(name, ball.hits)
		time.Sleep(100 * time.Millisecond)
		table <- ball
	}
}
```

## It's Easy to Go, But How to Stop
- Long-lived programs need to clean up.
- Let's look at how to write programs that handle communication, periodic events, and cancellation.
- The core is Go's `select` statement: like switch, but the decision is made based on the ability to communicate.

```go
select {
	case xc <- x:
		// sent x on xc
	case y := <-yc:
		// received y from yc
}
```

## Find an RSS Client
Searching godoc.org for "rss" turns up several hits, include one that provides:

```go
// Fetch fetches Item for uri and returns the time when the next
// fetch should be attempted. On failure, Fetch returns an error.
func Fetch(uri string) (items []Item, next time.Time, err error)

type Item struct {
	Title, Channel, GUID string // a subset of RSS fields
}
```
 
But I want a stream:

```go
<-chan Item
```

And I want multiple subscriptions.

## Here's What We Have

```go
type Fetcher interface {
	Fetch() (items []Item, next time.Time, err error)
}
func Fetch(domain string) Fetcher {...} // fetches Items from domain
```

## Here's What We Want

```go
type Subscription interface {
	Updates() <-chan Item // stream of Items
	Close() error // shuts down the stream
}
func Subscribe(fetcher Fetcher) Subscription {...} // converts Fetches to a stream
func Merge(subs ...Subscription) Subscription {...} // merges several streams
```

## Example

```go
func main() {
	// Subscribe to some feeds, and create a merged update stream.
	merged := Merge(
		Subscribe(Fetch("blog.golang.org")),
		Subscribe(Fetch("googleblog.blogspot.com")),
		Subscribe(Fetch("googledevelopers.blogspot.com")))

	// Close the subscriptions after some time.
	time.AfterFunc(3 * time.Second, func() {
		fmt.Println("closed:", merged.Close())
	})

	// Print the stream.
	for it := range merged.Updates() {
		fmt.Println(it.Channel, it.Title)
	}

	panic("show me the stacks")
}
```

## Implementing Subscription
To implement the __Subscription__ interface, define __Updates__ and __Close__.

```go
func (s *sub) Updates() <-chan Item {
	return s.updates
}

func (s *sub) Close() error {
	// TODO: make loop exit
	// TODO: find out about any error
	return err
}
```

## What Does Loop Do?
- Periodically call fetches
- Send fetched items on the Updates channel
- Exit when __Close__ is called, reporting any error

## Naive Implementation

```go
for {
	if s.closed {
		close(s.updates)
		return
	}
	items, next, err := s.fetcher.Fetch()
	if err != nil {
		s.err = err
		time.Sleep(10 * time.Second)
		continue
	}
	for _, item := range items {
		s.updates <- item
	}
	if now := time.Now(); next.After(now) {
		time.Sleep(next.Sub(now))
	}
}

func (s *naiveSub) Close() error {
	s.closed = true
	return s.err
}
```

 ## Bug 1: Unsynchronized Access to s.closed/s.err

```go
for {
```
  __if s.closed {__
```go
		close(s.updates)
		return
	}
	items, next, err := s.fetcher.Fetch()
	if err != nil {
```
  __s.err = err__
```go
		time.Sleep(10 * time.Second)
		continue
	}
	for _, item := range items {
		s.updates <- item
	}
	if now := time.Now(); next.After(now) {
		time.Sleep(next.Sub(now))
	}
}
```

```go
func (s *naiveSub) Close() error {
```
  __s.closed = true__
  __return s.err__
```go
}
```

## Race Detector
``` go run -race naivemain.go ```

```go
for {
```
  __if s.closed {__
```go
		close(s.updates)
		return
	}
	items, next, err := s.fetcher.Fetch()
	if err != nil {
```
  __s.err = err__

```go
func (s *naiveSub) Close() error {
```
  __s.closed = true__
  __return s.err__
```go
}
```

## Bug 2: time.Sleep May Keep Loop Running

```go
for {
	if s.closed {
		close(s.updates)
		return
	}
	items, next, err := s.fetcher.Fetch()
	if err != nil {
		s.err = err
```
  __time.Sleep(10 * time.Second)__
```go
		continue
	}
	for _, item := range items {
		s.updates <- item
	}
	if now := time.Now(); next.After(now) {
```
  __time.Sleep(10 * time.Second)__
```go
	}
}
```

## Bug 3: Loop May Block Forever on s.updates

```go
for {
	if s.closed {
		close(s.updates)
		return
	}
	items, next, err := s.fetcher.Fetch()
	if err != nil {
		s.err = err
		time.Sleep(10 * time.Second)
		continue
	}
	for _, item := range items {
```
  __s.updates <- item__
```go
	}
	if now := time.Now(); next.After(now) {
		time.Sleep(next.Sub(now))
	}
}
```

## Solution
Change the body of __loop__ to a __select__ with three cases:
- __Close__ was called
- It's time to call __Fetch__
- Send an item on __s.updates__

## Structure: for-select loop
- __Loop__ runs in its own goroutine.
- __Select__ lets __loop__ avoid blocking indefinitely in any one state.

```go
func (s *sub) loop() {
	// ... declare mutable state ...
	for {
		// ...set up channels for cases...
		select {
			case <-c1:
				// ...read/write state...
			case c2 <- x:
				// ...read/write state...
			case y := <-c3:
				// ...read/write state...
		}
	}
}
```
The cases interact via local state in __loop__.

## Case 1: Close
__Close__ communicates with __loop__ via __s.closing__.

```go
type sub struct {
	closing chan chan error
}
```

- The service (__loop__) listens for requests on its channel (__s.closing__)
- The client (__Close__) sends a request on __s.closing__: _exit and reply with the error_
- In this case, the only thing in the request is the _reply channel_.

__Close__ asks loop ti exit and waits for a response.

```go
func (s *sub) Close() error {
	errc := make(chan error)
	s.closing <- errc
	return <-errc
}
```

__loop__ handles __Close__ by replying with the __Fetch__ error and exiting.

```go
var err error // set when Fetch fails
for {
	select {
		case errc := <-s.closing:
			errc <- err
			close(s.updates) // tells receiver we're done
			return
	}
}
```

## Case 2: Fetch
Schedule the next __Fetch__ after some delay.

```go
var pending []Item // appended by fetch; consumed by send
var next time.Time // initially January 1, year 0
var err error
for {
	var fetchDelay time.Duration // initially 0 (no delay)
	if now := time.Now(); next.After(now) {
		fetchDelay := next.sub(now)
	}
	startFetch := time.After(fetchDelay)

	select {
		case <-startFetch:
			var fetched []Item
			fetched, next, err := s.fetcher.Fetch()
			if err != nil {
				next = time.Now().Add(10 * time.Second)
				break
			}
			pending = append(pending, fetched...)
	}
}
```

## Case 3: Send
Send the fetched items, one at a time.

```go
var pending []Item // appended by fetch; consumed by send
for {
	select {
		case s.updates <- pending[0]:
			pending = pending[1:]
	}
}
```
Whoops. This crashes.

## Select and nil channels
- Sends and receives on nil channels block.
- Select never selects a blocking case.

```go
func main() {
	a, b := make(chan string), make(chan string)
	go func() { a <- "a" }()
	go func() { b <- "b" }()
	if rand.IntN(2) == 0 {
		a = nil
		fmt.Println("nil a")
	} else {
		b = nil
		fmt.Println("nil b")
	}
	select {
		case s := <-a:
			fmt.Println("got", s)
		case s := <-b:
			fmt.Println("got", b)
	}
}
```

## Case 3: Send (fixed)
Enable send only when pending is non-empty.

```go
var pending []Item // appended by fetch; consumed by send
for {
	var first Item
	var updates chan Item
	if len(pending) > 0 {
		first = pending[0]
		updates = s.updates // enable send case
	}

	select {
		case updates <- first:
			pending = pending[1:]
	}
}
```

## Select
Put the three case together:

```go
select {
	case errc := <-s.closing:
		errc <- err
		close(s.updates)
		return
	case <-startFetch:
		var fetched []Item
		fetched, next, err = s.fetcher.Fetch()
		if err != nil {
			next = time.Now().Add(10 * time.Second)
			break
		}
		pending = append(pending, fetched...)
	case updates <- first:
		pending = pending[1:]
}
```

- The cases interact via err, next, and pending.
- No locks, no condition variables, no callbacks.

## Issue: Fetch May Return Deplicates

```go
var pending []Item
var next time.Time
var err error

case <- startFetch:
	car fetched []Item
	fetched, next, err = s.fetcher.Fetch()
	if err != nil {
		next = time.Now().Add(10 * time.Second)
		break
	}
	pending = append(pending, fetched...)
```

## Fix: Filter Items Before Adding to Pending

```go
var pending []Item
var next time.Time
var err error
var seen = make(map[string]bool) // set of items.GUIDs

case <-startFetch:
var fetched []Item
fetched, next, error = s.fetcher.Fetch()
if err != nil {
	next = time.Now().Add(10 * time.Second)
	break
}
for _, item := range fetched {
	if !seen[item.GUID] {
		pending = append(pending, item)
		seen[item.GUID] = true
	}
}
```

## Issue: Pending Queue Grows Without Bound

```go
case <- startFetch:
	var fetched []Item
	fetched, next, err = s.fetcher.Fetch()
	if err != nil {
		next = time.Now().Add(10 * time.Second)
		break
	}
	for _, item := range fetched {
		if !seen[item.GUID] {
			pending = append(pending, item)
			seen[item.GUID] = true
		}
	}
```

## Fix: Disable Fetch Case When Too Much Pending

```go
const maxPending = 10

var fetchDelay time.Duration
if now := time.Now(); next.After(now) {
	fetchDelay = next.Sub(now)
}
var startFetch <-chan time.Time
if len(pending) < maxPending {
	startFetch = time.After(fetchDelay) // enable fetch case
}
```

Could instead drop older items from the head of pending.

## Issue: Loop Blocks on Fetch

```go
case <- startFetch:
	var fetched []Item
	fetched, next, err = s.fetcher.Fetch()
	if err != nil {
		next = time.Now().Add(10 * time.Second)
		break
	}
	for _, item := range fetched {
		if !seen[item.GUID] {
			pending = append(pending, item)
			seen[item.GUID] = true
		}
	}
```

## Fix: Run Fetch Asynchronously
Add a new __select__ case for __fetchDone__.

```go
type fetchResult struct{ fetched []Item; next time.Time; err error }

var fetchDone chan fetchResult // if non-nil, Fetch is Running

var startFetch <- chan time.Time
if fetchDone == nil && len(pending) < maxPending {
	startFetch = time.After(fetchDelay) // enable fetch case
}

select {
	case <-startFetch:
		fetchDone = make(chan fetchResult, 1)
		go func() {
			fetched, next, err := s.fetcher.Fetch()
			fetchDone <- fetchResult{fetched, next, err}
		}()
	case result := <-fetchDone:
		fetchDone = nil
		// Use result.fetched, result.next, result.err
}
```

## Implemented Subscribe
- Responsive. Cleans up. Easy to read and change.
- Three technique:
  - __for-select__ loop
  - service channel, reply channels (```chan chan error```)
  - __nil__ channels in __select__ cases
More details online, including __Merge__.

## Conclusion
Concurrent programming can be tricky.
Go makes it easier:
- channels convey data, time events, cancellation signals
- goroutines serialize access to local mutable state
- stack traces & deadlock detector
- race detector
