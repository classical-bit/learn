def restore_documents(originals: tuple[str, ...], backups: tuple[str, ...]) -> set[str]:
    return set(map(str.upper, filter(lambda doc: not doc.isdigit(), originals + backups)))
