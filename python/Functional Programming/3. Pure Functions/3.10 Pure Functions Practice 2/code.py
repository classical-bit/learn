def sort_dates(dates: list[str]) -> list[str]:
    return sorted(dates, key=format_date)

def format_date(date: str) -> str:
    splits = date.split("-")
    return splits[2]+splits[0]+splits[1]
