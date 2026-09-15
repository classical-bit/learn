def zipmap(keys: list[str], values: list[float]) -> dict[str, float]:
    if len(keys) == 0 or len(values) == 0:
        return {}

    result = {keys[0]: values[0]}
    result.update(zipmap(keys[1:], values[1:]))

    return result

zipped: dict[str, float] = zipmap(
    [
        "Avatar: The Last Airbender",
        "Avatar (in Papyrus font)",
        "The Last Airbender (Live Action)",
    ],
    [9.9, 6.1, 2.1],
)

print(zipped)
# {
#   'Avatar: The Last Airbender': 9.9,
#   'Avatar (in Papyrus font)': 6.1,
#   'The Last Airbender (Live Action)': 2.1,
# }
