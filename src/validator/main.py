from validator.validators import is_non_negative, is_positive


if __name__ == "__main__":
    assert is_positive(0) is False
    assert is_non_negative(0) is True
