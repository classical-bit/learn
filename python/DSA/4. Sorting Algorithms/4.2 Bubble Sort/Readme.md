# Bubble Sort
Wait, if the standard `sorted()` function exists, why should we learn to write a sorting algorithm from scratch?

In this chapter we'll be building some of the most famous sorting algorithms from scratch because:

- It's good to undetstand how they work under the hood
- It's great algorithmic thinking practice
- It's fun!

Bubble sort is a very basic sorting algorithm named for the way elements "bubble up" to the top of the list.

Bubble sort repeatedly steps through a slice and compares adjacent elements, swapping them if they are out of order. It continues to loop over the slice until the whole list is completely sorted. Here's a pseudocode:

1. Set `swapping` to `True`
2. Set `end` to the length of the input list
3. While `swapping` is `True`:
  1. Set `swapping` is `False`
  2. For `i` from the 2nd element to `end`:
    - If the `(i-1)`th element of the input list is greater than the `i`th element:
      1. Swap the `(i-1)`th element and the `i`th element
      2. Set `swapping` to `True`
  3. Decrement `end` by one
4. Return the sorted list
