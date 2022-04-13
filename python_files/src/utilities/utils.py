
def as_float(logger, string, or_else: float = 0, not_less_than: float = 0) -> float:
    try:
        return max(float(string), not_less_than)
    except ValueError:
        logger(f'Value error when parsing {string}, fallback to {or_else}')
        return max(or_else, not_less_than)
