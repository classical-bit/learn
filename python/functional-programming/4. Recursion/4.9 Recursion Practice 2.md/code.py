def count_nested_levels(
    nested_documents: dict[int, dict], target_document_id: int, level: int = 1
) -> int:
    for doc_id, nested_dict in nested_documents.items():
        if doc_id == target_document_id:
            return level

        found_level = count_nested_levels(nested_dict, target_document_id, level + 1)

        if found_level != -1:
            return found_level

    return -1


nested_docs: dict[int, dict] = {1: {3: {}}, 2: {4: {}, 5: {6: {7: {8: {9: {10: {}}}}}}}}

print(count_nested_levels(nested_docs, 1))
# 1
print(count_nested_levels(nested_docs, 2))
# 1
print(count_nested_levels(nested_docs, 3))
# 2
print(count_nested_levels(nested_docs, 4))
# 2
print(count_nested_levels(nested_docs, 5))
# 2
print(count_nested_levels(nested_docs, 6))
# 3
print(count_nested_levels(nested_docs, 7))
# 4
print(count_nested_levels(nested_docs, 8))
# 5
print(count_nested_levels(nested_docs, 9))
# 6
print(count_nested_levels(nested_docs, 10))
# 7
