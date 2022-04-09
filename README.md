# env_var

A simple utility for working with environment variables. The main goal was to provide proper type check.

```python
from env_var import env

minio_port = env('PORT').as_port_number().default(9000).required() # port type hint is `int`
minio_host = env('MINIO_HOST').as_hostname().optional() # minio_host type hint is `str | None`
minio_secure = env('MINIO_SECURE').as_bool().required() # minio_host type hint is `bool`
```

Setting `default` will result in always returning a value, so it makes little sense to use it with `optional`.
