# env_var

A simple utility for working with environment variables. The main goal was to provide proper type check.

```python
from env_var import env

port = env('PORT').as_port_number().required() # port type hint is `int`

minio_host = env('MINIO_HOST').as_hostname().optional() # minio_host type hint is `str | None`
```

## Type Hints

```python
from typing import overload, Literal, Optional

@overload
def get_something() -> Optional[str]: ...
@overload
def get_something(required: Literal[False]) -> Optional[str]: ...
@overload
def get_something(required: Literal[True]) -> str: ...
def get_something(required: bool = False) -> Optional[str]:
  if required: return "ok"

something = get_something()
something = get_something(required=False)
something = get_something(required=True)
```