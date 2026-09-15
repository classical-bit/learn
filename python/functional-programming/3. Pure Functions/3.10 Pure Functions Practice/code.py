from collections.abc import Callable

default_commands: dict[str, Callable[..., object]] = {}
default_formats: list[str] = ["txt", "md", "html"]
saved_documents: dict[str, str] = {}

# Don't edit above this line


def add_custom_command(
    commands: dict[str, Callable[..., object]],
    new_command: str,
    function: Callable[..., object],
) -> dict[str, Callable[..., object]]:
    new_commands: dict[str, Callable[..., object]] = commands.copy()
    new_commands[new_command] = function
    return new_commands


def add_format(formats: list[str], format: str) -> list[str]:
    new_formats = formats.copy()
    new_formats.append(format)
    return new_formats


def save_document(docs: dict[str, str], file_name: str, doc: str) -> dict[str, str]:
    new_docs = docs.copy()
    new_docs[file_name] = doc
    return new_docs


def add_line_break(line: str) -> str:
    return line + "\n\n"
