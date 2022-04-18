# env_var

A simple utility for working with environment variables. The main goal was to provide proper type check.

## Installation

```bash
pip install env-var
```

## Usage

```python
from env_var import env

minio_port = env('MINIO_PORT').as_port_number().default(9000).required() # port type hint is `int`
minio_host = env('MINIO_HOST').as_hostname().optional() # minio_host type hint is `str | None`
minio_secure = env('MINIO_SECURE').as_bool().required() # minio_host type hint is `bool`
```

Setting `default` will result in always returning a value, so it makes little sense to use it with `optional`.


It might be useful to gather all environment variables that are used in an application to a separate file.

```python
from enum import Enum
from env_var import env

class SomeImportantOption(Enum):
  option_a = "a"
  option_b = "b"
  option_c = "c"

PG_HOST = env('PG_HOST').as_hostname().required()
PG_PORT = env('PG_PORT').as_port_number().default(5432).required()
PG_DB = env('PG_DB').as_string().required()
PG_USER = env('PG_USER').as_string().required()
PG_PASSWORD = env('PG_PASSWORD').as_string().required()

IMPORTANT_OPTION = env('IMPORTANT_OPTION').as_enum(SomeImportantOption).required()
```
Sometimes it might happen that some variables will be required only in specific circumstances, in such cases calling `required` can be postponed until the variable is actually needed.

```python
UPDATE_URL = env('UPDATE_URL').as_url()
"""required only when some condition is met"""

# elsewhere in the code
def send_update(status: str):
  url = UPDATE_URL.required()
  requests.post(url, dict(status=status))
```

It's also possible to pass custom transformers/validators.

```python
@dataclass
class MyOwnClass:
    initial: str

initial_class = env("INITIAL").custom_transformer(MyOwnClass).required() # intial_class is of type MyOwnClass
```
