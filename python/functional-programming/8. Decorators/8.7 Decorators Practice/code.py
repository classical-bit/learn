from collections.abc import Callable

TextFunc = Callable[[str], str]

# Don't touch above this line


def replacer(old: str, new: str) -> Callable[[TextFunc], TextFunc]:
    def replace(decorated_func: TextFunc) -> TextFunc:
        def wrapper(text: str) -> str:
            modified_text = text.replace(old, new)
            return decorated_func(modified_text)

        return wrapper

    return replace

@replacer("&", "&amp;")
@replacer("<", "&lt;")
@replacer(">", "&gt;")
@replacer('"', "&quot;")
@replacer("'", "&#x27;")
def tag_pre(text: str) -> str:
    return f"<pre>{text}</pre>"  # Don't change the body of tag_pre

input_text = "5 > 3 & 2 < 4, \"Hello 'World'\""

result = tag_pre(input_text)

print(result)
# <pre>5 &gt; 3 &amp; 2 &lt; 4, &quot;Hello &#x27World&#x27;&quot;</pre>
