# Insertion Sort
Insertion sort builds a sorted list one item at a time. It's much less efficient on large lists than merge sort because it's `O(n^2)`, but it's actually faster (not in Big O terms, but due to smaller constants) than merge sort on small lists.

# Assignment
Our influencers want to sort their affiliate deals by revenue. None of our users have more than a couple hundred affiliate deals, so we don't __need__ an `n * log(n)` algorithm like merge sort. In fact, `insertion_sort` can be faster than `merge_sort`, and uses less of our server's memory.

Complete the `insertion_sort` funciton according to the given pseudocode:

1. For each index in the input list, starting with the second element:
  1. Set a `j` variable to the current index
  2. While `j` is greater than `0` and the element at index `j-1` is greater than the element at index `j`:
    1. Swap the elements at indices `j` and `j-1`
    2. Decrement `j` by `1`
2. Return the list
