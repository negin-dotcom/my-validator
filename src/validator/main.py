import re

from validator.validators import matches


if __name__ == "__main__":
    assert matches("[abc", r"\d+") is False
