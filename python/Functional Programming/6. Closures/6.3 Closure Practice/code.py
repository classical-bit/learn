from collections.abc import Callable


def new_collection(initial_docs: list[str]) -> Callable[[str], list[str]]:
    new_docs = initial_docs.copy()
    def add_doc(s: str) -> list[str]:
        new_docs.append(s)
        return new_docs
    return add_doc

my_initial_docs = ["doc1", "doc2", "doc3"]
my_collection: Callable[[str], list[str]] = new_collection(my_initial_docs)
print(my_collection("doc4"))
# ['doc1', 'doc2', 'doc3', 'doc4']
print(my_collection("doc5"))
# ['doc1', 'doc2', 'doc3', 'doc4', 'doc5']
print(my_initial_docs)
# ['doc1', 'doc2', 'doc3']
