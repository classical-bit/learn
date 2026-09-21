# LRU Cache
Least Recently Used (LRU) is a cache eviction policy that keeps track of how recently data is used. When the cache has no space for new data, it removes the item that has not been accessed for the longest time and stores the new item instead.

- Frequently accessed data is given higher priority in the cache because it has a strong chance of being needed again soon.
- Data that stays unused for a long time is assigned lower priority and is removed first when the cache becomes full.

> __Example__: If a cache can store 3 pages and the access sequence is A -> B -> C -> A -> D, page B is evicted because it is the least recently used (LRU) item.

## Operations on LRU Cache
These operations help manage data efficiently in the cache by storing, accessing, updating, and removing items based on their recent usage.

- LRU Cache (capacity c): Initializes the LRU cache with a fixed capacity c.
- get(key): Returns the value associated with the given key if it exists in the cache; otherwise, returns -1. The accessed item is marked as the most recently used.
- put(key, value): Inserts a new key-value pair or updates the value of an existing key. If the cache exceeds its capacity, the least recently used item is removed.

## Working of LRU Cache
Let's suppose we have an LRU cache of capacity 3, and we would like to perform the following operations:

Cache []
- put (key=1, value=A) into the cache
Cache [1: A]
- put (key=2, value=B) into the cache
Cache [2: B, 1: A]
- put (key=3, value=C) into the cache
Cache [3: C, 2: B, 1: A]
- get (key=2) from the cache
Cache [2: B, 3: C, 1: A]
- get (key=4) from the cache
Cache [2: B, 3: C, 1: A]
- put (key=4, value=D) into the cache
Cache [4: D, 2: B, 3: C]
- put (key=3, value=E) into the cache
Cache [3: E, 4: D, 2: B]
- get (key=4) from the cache
Cache [4: D, 3: E, 2: B]
- put (key=1, value=A) into the cache
Cache [1: A, 4: D, 3: E]

## Designing LRU Cache
Design a data structure for LRU Cache. It should support the following operations: __get__ and __put__.
- __get(key)__ - Returns the value of the given key if it exists in the cache; otherwise, returns -1.
- __put(key, value)__ - Inserts or updates the key-value pair in the cache. If the cache reaches capacity, remove the least recently used item before adding the new item.

### Naive Approach 1 - LRU Cache using an Array of Nodes - O(n) Time and O(n) Space:
The idea is to implement using an __array__ to store nodes, where each node holds a key-value pair. The primary operations, __get__ and __put__, are performed with __O(n)__ time complexity due to the need to search through the array. The size of the array will be equal to the given capacity of the cache.

- __put(int key, int value)__
  - If te cache is full, find the node with the oldest timestamp (least recently used) and replace this node with the new key and value.
  - else, simply add the new node to the end of the array with the timestamp of insertion.
  - __Time Complexity__: O(n) (because you might have to search for the oldest node)
- __get(int key)__
  - Search through the array for the node with the matching key.
  - If found, update its timestamp and return its value, else return -1.
  - __Time Complexity__: O(n) (because you might have to check every node)

We initialize an array of size equal to that of our cache. Here each data element stores extra information to mark with an access __time stamp__. It shows the time at which the key is stored. We wull use the timeStamp to find out the __least recently used__ element in the LRU cache.

```go
type Node struct {
	key int
	value int
	timeStamp time.Time
}

type LRUCache struct {
	capacity int
	nodes []Node
}

func NewLRUCache(capacity int) *LRUCache {
	return &LRUCache{
		capacity: capacity,
		nodes: make([]Node, 0, capacity),
	}
}

func (c *LRUCache) Get(key int) int {
	for i := range c.nodes {
		if c.nodes[i].key == key {
			c.nodes[i].timeStamp = time.Now()
			return c.nodes[i].value
		}
	}
	return -1
}

func (c *LRUCache) Put(key int, value int) {
	now := time.Now()

	// Case 1: Key already exists -> update value and timestamp
	for i := range c.nodes {
		if c.nodes[i].key == key {
			c.nodes[i].value = value
			c.nodes[i].timeStamp = now
			return
		}
	}

	// Case 2: Cache is not full -> append new node
	if len(c.nodes) < c.capacity {
		c.nodes = append(c.nodes, Node{
			key: key,
			value: value,
			timeStamp: now,
		})
		return
	}

	// Case 3: Cache is full -> find node with the oldest timestamp and replace it
	lruIndex := 0
	for i := 1; i < len(c.nodes); i++ {
		if c.nodes[i].timeStamp.Before(c.nodes[lruIndex].timeStamp) {
			lruIndex = i
		}
	}

	c.nodes[lruIndex] = Node{
		key: key,
		value: value,
		timeStamp: now,
	}
}
```

### Naive Approach 2 - LRU Cache using Singly Linked List - O(n) Time and O(n) Space:
The approach to implement an LRU (Least Recently Used) cache involves using a singly linked list to maintain the order of cache entries.

- __get operation__: The cache searches for the node with the requested key by traversing the list from the head. If the key is found, the node is moved to the head of the list to mark it as the most recently used, and its value is returned. else, returns -1. This operation has a time complexity of __O(n)__ because it may require scanning through the entire list.
- __put operation__: The cache inserts a new key-valye pair at the head of the list if the cache has not reached its capacity. If the key already exists, the corresponding node is found and updated, then moved to the head. When the cache reaches its capacity, the least recently used element, which is located at the tail of the list, is removed. The time complexity for this operation is also __O(n)__ due to the traversal and reordering steps involved.

```go
type Node struct {
	key int
	value int
	next *Node
}

type LRUCache struct {
	head *Node
	capacity int
	size int
}

func NewLRUCache(capacity int) *LRUCache {
	return &LRUCache {
		head: nil,
		capacity: capacity,
		size: 0
	}
}

func (c *LRUCache) Get(key int) int {
	if c.head == nil {
		return -1
	}

	// Case 1: Key is already at the head
	if c.head.key == key {
		return c.head.value
	}

	// Case 2: Key is deeper in the list
	prev := c.head
	curr := c.head.next

	for curr != nil {
		if curr.key == key {
			// Unlink curr from its current position
			prev.next = curr.next

			// Move curr to the head
			curr.next = c.head
			c.head = curr

			return curr.val
		}
		prev = curr
		curr = curr.next
	}

	return -1
}

func (c *LRUCache) Put(key int, val int) {
	// Case 1: Key already exists in the cache
	if c.head != nil {
		// Sub-case 1a: Key is at the head
		if c.head.key == key {
			c.head.val = val
			return
		}

		// Sub-case 1b: Key is deeper in the list
		prev := c.head
		curr := c.head.next

		for curr != nil {
			if curr.key == key {
				curr.val = val

				// Unlink curr for current position
				prev.next = curr.next

				// Move curr to head
				curr.next = c.head
				c.head = curr
				return
			}
			prev = curr
			curr = curr.next
		}
	}

	// Case 2: Key does not exist and cache is full -> Evict the tail node (LRU)
	if c.size == c.capacity {
		if c.capacity == 1 {
			c.head = nil
		} 
		else {
			// Traverse to second-to-last node
			curr := c.head
			for curr.next != nil && curr.next.next != nil {
				curr = curr.next
			}
			// Remove tail
			// curr.next = nil
		}
		c.size--
	}

	// Case 3: Insert the new key-value pair at the head
	c.head = &Node{
		key: key,
		val: val,
		next: c.head
	}
	c.size++
}
```

### Expected Approach - LRU Cache using Doubly Linked List and Hashing - O(1) Time and O(1) Space:
The basic idea behind implementing an LRU cache using a key-value pair approach is to manage element access and removal efficiently through a combination of a doubly linked list and a hash map.
- When adding a new key-value pair, insert it as a new node at the __head__ of the doubly linked list. This ensures that the newly added key-value pair is marked as the most recently used.
- If the key is already present in the cache, get the corresponding node in the doubly linked list using hashmap, update its value and move it to the head of the list.
- When the cache reaches its maximum capacity and a new key-value pair need to be added, remove the node from the tail in the doubly linked list. and map as well.

```go
// To make pointer operations clean and avoid edge-cases null checks, this implementation uses dummy head and tail nodes.
type Node struct {
	key int
	val int
	prev *Node
	next *Node
}

type LRUCache struct {
	capacity int
	cache map[int]*Node
	head *Node
	tail *Node
}

func NewLRUCache(capacity int) *LRUCache {
	lru := &LRUCache{
		capacity: capacity,
		cache: make(map[int]*Node),
		head: &Node{},
		tail: &Node{},
	}

	// Link dummy head and tail together
	lru.head.next = lru.tail
	lru.tail.prev = lru.head

	return lru
}

func (c *LRUCache) addNode(node *Node) {
	node.prev = c.head
	node.next = c.head.next

	c.head.next.prev = node
	c.head.next = node
}

func (c *LRUCache) removeNode(node *Node) {
	prev := node.prev
	next := node.next

	prev.next = next
	next.prev = prev
}

func (c *LRUCache) moveToHead(node *Node) {
	c.removeNode(node)
	c.addNode(node)
}

func (c *LRUCache) popTail() *Node {
	lru := c.tail.prev
	c.removeNode(lru)
	return lru
}

func (c *LRUCache) Get(key int) int {
	if node, ok := c.cache[key]; ok {
		c.moveToHead(node)
		return node.val
	}
	return -1
}

func (c *LRUCache) Put(key int, val int) {
	// Case 1: Key exists -> update value and move to head
	if node, ok := c.cache[key]; ok {
		node.val = val
		c.moveToHead(node)
		return
	}

	// Case 2: Key is new -> check capacity
	if len(c.cache) == c.capacity {
		// Remove LRU element from list and hash map
		lru := c.popaTail()
		delete(c.cache, lru.key)
	}

	// Create and insert new node at head
	newNode := &Node{key: key, val: val}
	c.cache[key] = newNode
	c.addNode(newNode)
}
```
