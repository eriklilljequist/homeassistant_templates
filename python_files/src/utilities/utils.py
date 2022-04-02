
def as_float(logger, string, or_else=None, not_less_than=None):
    try:
        return max(float(string), not_less_than)
    except ValueError:
        logger(f'Value error when parsing {string}, fallback to {or_else}')
        return float(or_else)
