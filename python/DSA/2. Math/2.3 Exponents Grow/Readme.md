# Exponents Grow
Exponents grow very large very quickly. Let's take a look at an example of them doing that, in code.

## Assignment
While the influencers who use our platform are really great at taking selfies, most aren't super great at math. We need to write a tool that predicts an influencer's follower growth over time.

Complete the `get_follower_prediction` function. It takes a `follower_count` integer, an `influencer_type` string and a `num_months` integer, and returns an integer.

Calculate the number of followers an influencer will have after a given number of months according to the influencer type:

- "fitness": follwer count __quadruples__ each month
- "cosmetic": follwer count __triples__ each month
- __other__: follower count __doubles__ each month

For example, if a `"fitness"` influencer starts with `10` followers, then after `1` month they would have `40` followers. After `2` months, they would have `160` followers, and so on.

This kind of sequence, where each term is found by multiplying the previous term by a constant, is called a geometric sequence or geometric progression.

Use the following version of the geometric progression formula, in which `a1` is the initial number of followers, `r` is the multiplication constant, and `n` is the number of months.

```
total = a1 * r^n
```
