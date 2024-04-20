def type_error(t1, t2) -> str:
    return f'Unexpected type. Expected {t1}, got {t2}.'


def val_too_low_error(m: float) -> str:
    return f'Unexpected value. Value should be greater than {m}.'


def val_too_high_error(m: float) -> str:
    return f'Unexpected value. Value should be less than {m}.'


def val_bool_error(b: bool) -> str:
    return f'Unexpected value. Expected {b}, got {not b}.'


def val_not_equal_error(n1, n2) -> str:
    return f'Unexpected value. Expected {n1}, got {n2}.'
