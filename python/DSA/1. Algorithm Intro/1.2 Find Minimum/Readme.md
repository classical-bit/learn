# Find Minimum
In this course, we'll write algorithms for LockedIn: a fictitious social media app for professionals to virtue signal about how all the for-profit work they do is actually an altruistic endeavor.

## Assignment
We need to show our users which people they follow have the lowest follower counts. That way they'll know when the people they follow aren't popular enough to be worth following anymore.

__Implement the "find minimum" algorithm__ on the right by completing the `find_minimum()` function. It accepts a list of integers `nums` and returns the smallest number in the list.

1. Set `minimum` to positive infinity: `float("inf")`.
2. If the list is empty, return `None`.
3. For each number in the list `nums`, compare it to `minimum`. If the number is smaller than `minimum`, set `minimum` to that number.
4. `minimum` is now set to the smallest number in the list, so `return` it.
