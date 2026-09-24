from collections.abc import Callable

PluginConfig = dict[str, str | None]
PluginFunc = Callable[..., PluginConfig]

# Don't touch above this line


def configure_plugin_decorator(func: PluginFunc) -> PluginFunc:
    def wrapper(*args: tuple[str, str | None]) -> PluginConfig:
        return func(**dict(args))
    return wrapper

@configure_plugin_decorator
def configure_backups(path: str, prefix: str, extension: str) -> PluginConfig:
    return {
        "path": path,
        "prefix": prefix,
        "extension": extension,
    }

plugin_config: PluginConfig = configure_backups(
    ("path", "~/duplicates"),
    ("prefix", "duplicates_"),
    ("extension", ".rtf")
)

print(plugin_config)
# {
#   'path': '~/duplicates',
#   'prefix': 'duplicates_',
#   'extension': '.rtf'
# }
