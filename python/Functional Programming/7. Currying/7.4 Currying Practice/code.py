from collections.abc import Callable


def create_markdown_image(alt_text: str) -> Callable[[str], Callable[..., str]]:
    _alt_text = f"![{alt_text}]"
    def enclose_url(url: str) -> Callable[[str], str]:
        escaped_url = url.replace("(", "%28").replace(")", "%29")
        _url = f"({escaped_url})"

        def enclose_title(title: str|None = None) -> str:
            nonlocal _url
            if title:
                _url = f"{url[0:-1]} \"{title}\")"
            return _alt_text + _url

        return enclose_title

    return enclose_url

print(create_markdown_image("This is Alt text")("(http://example.com)")("Example Image"))
# ![This is Alt Text](http://example.com "Example Image")
