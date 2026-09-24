from collections.abc import Callable
from functools import reduce


def lines_with_sequence(char: str) -> Callable[[int], Callable[[str], int]]:
    def with_char(length: int) -> Callable[[str], int]:
        sequence = char * length
        def with_length(doc: str) -> int:
            return reduce(lambda c, line: c+1 if sequence in line else c, doc.splitlines(), 0)

        return with_length

    return with_char

my_doc: str = """aaaa
bbbb
ccdd
aabb"""

print(lines_with_sequence("b")(2)(my_doc))
# 2
