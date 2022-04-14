class EnvVarNotDefinedError(Exception):
    """
    Exception raised when env var is not set
    """

    def __init__(self, var_name: str) -> None:
        super().__init__(f'env var "{var_name}" should be defined')


class EnvVarValidationError(Exception):
    """
    Exception raised when env var is not valid
    """

    def __init__(self, var_name: str, *args) -> None:
        msg = None
        if len(args) > 0:
            msg = args[0]
        super().__init__(
            ": ".join(
                filter(None, [f'error while validating env var "{var_name}"', msg])
            )
        )
