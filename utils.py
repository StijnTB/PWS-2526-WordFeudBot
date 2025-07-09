def floor(number: float) -> int:
    if round(number) - number > 0:
        return number - (round(number) - number)
    else:
        return round(number)

def ceil(number: float) -> int:
    if round(number) - number > 0:
        return round(number)
    else:
        return number - (round(number) - number)