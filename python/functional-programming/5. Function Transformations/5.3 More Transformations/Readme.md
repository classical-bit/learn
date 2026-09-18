# More Transformations
Complete the `doc_format_checker_and_converter` function. It takes a `conversion_function` and a list of `valid_formats` as parameters. It should return a new function that takes two parameters of its own:
- `filename`: The name of the file to be converted
- `content`: The content (body text) of the file to be converted

1. If the file extension of the `filename` is in the `valid_formats` list, then return the result of the `conversion_function` on the `content`.
2. Otherwise, raise a ValueError with the message "invalid file format".
