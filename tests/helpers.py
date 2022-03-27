import os
from typing import Optional

VAR_NAME = "TEST_VAR"


def set_var(val: Optional[str] = None):
    os.environ[VAR_NAME] = val
