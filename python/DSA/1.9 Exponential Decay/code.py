def decayed_followers(
    initial_followers: int, fraction_lost_daily: float, days: int
) -> float:
    return initial_followers * pow(1-fraction_lost_daily, days)
