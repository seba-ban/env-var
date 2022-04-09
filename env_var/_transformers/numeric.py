from typing import Optional, Type, TypeVar

NumericType = TypeVar("NumericType", int, float)


def num_transformer_factory(
    type_: Type[NumericType],
    min: Optional[NumericType] = None,
    max: Optional[NumericType] = None,
    base: Optional[int] = None,
):
    if min is not None and max is not None and min > max:
        raise ValueError("min should be less than max")

    if base is not None and type_ is float:
        raise ValueError("base can be only defined for int")

    def transformer(s: str) -> NumericType:

        if base is None:
            val = type_(s)
        else:
            val = type_(s, base=base)  # type: ignore

        if min is not None and val < min:
            raise ValueError(f"should be bigger or equal {min}")

        if max is not None and val > max:
            raise ValueError(f"should be less or equal {max}")

        return val

    return transformer
