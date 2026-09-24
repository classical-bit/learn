# Function Transformations Practice
In Doc2Doc, users are asking for a filtering feature. They want a command that has dynamic options so that they can work as quickly as possible.

Complete the `get_filter_cmd` function. It takes two functions as input, `filter_one` and `filter_two`, and retuns a function, `filter_cmd`.

`filter_cmd` itself should take as input two strings: `content` and `option`.

1. Set the default value of the `option` argument to `"--one"`.
2. Complete `filter_cmd` so that it filters and returns the `content` according to the input `option`.
  1. if `"--one"`, use `filter_one`.
  1. if `"--two"`, use `filter_two`.
  1. if `"--three"`, use `filter_one` first, then `filter_two`.
  1. if any other `option` is passed, raise an exception "invalid option"
