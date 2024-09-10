import typing as t


def count_decimal_places(value: t.Union[float, int]):
    if isinstance(value, int):
        value = float(value)
    return str(value)[::-1].find('.')
