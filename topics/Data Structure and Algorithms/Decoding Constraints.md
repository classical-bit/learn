# Decoding Constraints
In Data Structures and Algorithm (DSA), constraints act as a reverse-engineered roadmap to the expected `time complexity`, which immediately eliminates wrong patterns and highlights the right one.

## Decoding N (Input Size) to Find Time Complexity
Computer processors roughly handle 10^7 to 10^8 operations per second safely under a 1-second time limit. By looking at the maximum value of N, you can deduce the required algorithmic complexity:
- N <= 12 to 20 -> O(2^N) or O(N!):
  - Hidden Pattern: __Backtracking__, __Recursion__, or __Bitmasking__.
  - Why: An exponential complexity like 2^20 ~= 10^6, which passes easily. An O(N^2) or O(N^3) here is overkill, but N=100 will TLE (Time Limit Exceeded) for 2^N.

- N <= 100 to 400 -> O(N^3):
  - Hidden pattern: __Triple nested loops__ or small-scale __Dynamic Progamming (DP)__.
  - Why: 400^3 ~= 6.4 * 10^7, fitting right inside the time budget.

- N <= 1000 to 5000 -> O(N^2):
  - __2D Dynamic Programming__, nested iteration, or checking all pairs.
  - Why: 5000^2 = 2.5 * 10^7 operations.

- N <= 10^5 to 10^6 -> O(NlogN) or O(N):
  - Hidden Pattern: __Sorting__, __Two Pointers__, __Sliding Window__, __Priority Queue (Heap)__, or standar __BFS/DFS__.
  - Why: 10^6log(10^6) ~= 2 * 10^7 operations. An O(N^2) solution (10^12 ops) will instantly fail.

- N > 10^8 -> O(logN) or O(1):
  - Hidden Pattern: __Binary Search__ or __Mathematical formulas__.
  - Why: Linear scan O(N) is too slow; you need logarithmic scaling.
