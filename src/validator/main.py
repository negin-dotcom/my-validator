import re

from validator.validators import is_int


if __name__ == "__main__":
    assert is_int(5.0) is True
