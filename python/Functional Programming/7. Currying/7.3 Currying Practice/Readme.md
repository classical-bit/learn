# Currying Practice
Remember, currying is when we take a function that accepts multiple arguments:

```python
final_volume: int = box_volume(3, 4, 5)
print(final_volume)
# 60
```

and convert it into a series of functions that each accept a single argument:

```python
final_volume: int = box_volume(3)(4)(5)
print(final_volume)
# 60
```

- `box_volume(3)` returns a new function that accepts a single integer and returns a new function.
- `box_volume(3)(4)` returns another new function that accepts a single integer and returns the final result.
- `box_volume(3)(4)(5) returns the final result.

Here's another way of calling it, where each function is stored in a variable before being called:

```python
with_length_3 = box_volume(3)
with_len_3_width_4 = with_length_3(4)
final_volume = with_len_3_width_4(5)
print(final_volume)
# 60
```

Here are function definitions:

```python
from collections.abc import Callable

def box_volume(length: int) -> Callable[[int], Callable[[int], int]]:
    def box_volume_with_len(width: int) -> Callable[[int], int]:
        def box_volume_with_len_width(height: int) -> int:
            return length * width * height

        return box_volume_with_len_width

    return box_volume_with_len
```
