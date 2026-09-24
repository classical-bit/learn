# Closure Practice
Remember, a closure is a function that retains the state of its environment. That makes it useful for tracking data as it changes over time, but it can come at the cost of understandibility.

When not to use the nonlocal keyword: when the variable is mutable - such as a list, dictionary, or set - and you're modifying its contents rather than reassigning the variable. You only need nonlocal if you're reassigning a variable (which you must do to update immutable values like strings and integers)
