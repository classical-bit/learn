def find_longest_word(document: str, longest_word: str = "") -> str:
    if document == "":
        return longest_word

    splits = document.split(" ", maxsplit=1)
    word = splits[0]
    rest = splits[1] if len(splits) > 1 else ""
    if len(word) > len(longest_word):
        longest_word = word
    return find_longest_word(rest, longest_word)

print(find_longest_word("How are you?"))
# you?
