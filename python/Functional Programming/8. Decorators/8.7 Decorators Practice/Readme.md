# Decorators Practice
You can stack decorators, and you can use currying with decorators.

```python
from collections.abc import Callable

TextFunc = Callable[[str], None]

def to_uppercase(func: TextFunc) -> TextFunc:
    def wrapper(document: str) -> None:
        func(document.upper())

    return wrapper

def get_truncate(length: int) -> Callable[[TextFunc], TextFunc]:
    def truncate(func: TextFunc) -> TextFunc:
        def wrapper(document: str) -> None:
            func(document[:length])

        return wrapper

    return truncate

@to_uppercase
@get_truncate(9) # currying
def print_input(input: str) -> None:
    print(input)

print_input("Keep Calm and Carry On")
# prints: "KEEP CALM"
```

Notice that `get_truncate(9)` first returns a decorator, which wraps `print_input`. Then `to_uppercase` wraps that already-wrapped function. When `print_input` is called, the text is converted to uppercase, then truncated to 9 characters before printing.
