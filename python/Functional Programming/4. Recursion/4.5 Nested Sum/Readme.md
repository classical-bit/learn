# Nested Sum
Recursion is hard for all new developers. If you're struggling, that's okay! Take your time. That's why we're doing a few extra practice problems.

In Doc2Doc, users can process files or entire directories. We need to know the total size of those files and directories (measured in bytes).

Due to the nested nature of directories, we represent a root directory as a list of lists. Each list represents a directory, and each number represents the size of a file in that directory. For example, here's a directory that contains 2 files at the root level, then a nested directory with its own two files:

```python
root: list[int | list] = [1, 2, [3, 4]]
print(sum_nested_list(root))
# 10
```

Here's a more complex example:

```
root
├── scripts.txt (5 bytes)
├── characters (dir)
│   ├── zuko.txt (6 bytes)
│   └── aang.txt (7 bytes)
└── seasons (dir)
    ├── season1 (dir)
    │   ├── the_avatar_returns.docx (8 bytes)
    │   └── the_southern_air_temple.docx (9 bytes)
    └── season2_notes.txt (10 bytes)
```

which would be represented as:

```python
root: list[int | list] = [5, [6, 7], [[8, 9], 10]]
print(sum_nested_list)
# 45
```
