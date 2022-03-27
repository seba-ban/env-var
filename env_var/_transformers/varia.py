from fqdn import FQDN


def fqdn_transformer(s: str):
    fqdn = FQDN(s)
    if not fqdn.is_valid:
        raise ValueError(f"{s} is not a valid FQDN")
    return fqdn
