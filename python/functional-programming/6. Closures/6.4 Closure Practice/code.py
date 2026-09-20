import copy
from collections.abc import Callable

Styles = dict[str, dict[str, str]]

# Don't touch above this line

def css_styles(initial_styles: Styles) -> Callable[[str, str, str], Styles]:
    new_styles = copy.deepcopy(initial_styles)
    if not new_styles:
        new_styles = {}
    def add_style(selector: str, property: str, value: str) -> Styles:
        if selector not in new_styles:
            new_styles[selector] = {property: value}
        else:
            new_styles[selector].update({property: value})
        return new_styles

    return add_style

initial_styles: dict[str, dict[str, str]] = {
    "body": {"background-color": "white", "color": "black"},
    "h1": {"font-size": "16px", "padding": "10px"},
}

add_style: Callable[[str, str, str], dict[str, dict[str, str]]] = css_styles(
    initial_styles
)

new_styles: dict[str, dict[str, str]] = add_style("p", "color", "grey")
print(new_styles)
# {
#    "body": {
#        "background-color": "white",
#        "color": "black"
#    },
#    "h1": {
#        "font-size": "16px",
#        "padding": "10px"
#    },
#    "p": {
#        "color": "grey",
#    }
# }

print(add_style("p", "border", "1px solid black"))
# {
#    "body": {
#        "background-color": "white",
#        "color": "black"
#    },
#    "h1": {
#        "font-size": "16px",
#        "padding": "10px"
#    },
#    "p": {
#        "color": "grey",
#        "border": "1px solid black"
#    }
# }
