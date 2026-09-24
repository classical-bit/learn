def sum_nested_list(lst: list[int | list]) -> int:
    if len(lst) == 0:
        return 0

    sum = 0
    for item in lst:
        if isinstance(item, int):
            sum += item
        else:
            sum += sum_nested_list(item)
    return sum

root: list[int | list] = [5, [6, 7], [[8, 9], 10]]
print(sum_nested_list(root))
# 45
