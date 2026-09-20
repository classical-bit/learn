from collections.abc import Callable


def doc_format_checker_and_converter(
    conversion_function: Callable[[str], str], valid_formats: list[str]
) -> Callable[[str, str], str]:
    def inner_func(filename: str, content: str) -> str:
        format = filename.split(".")[1]
        if format in valid_formats:
            return conversion_function(content)
        raise ValueError("invalid file format")
    return inner_func

# Don't edit below this line

def capitalize_content(content: str) -> str:
    return content.upper()

def reverse_content(content: str) -> str:
    return content[::-1]
