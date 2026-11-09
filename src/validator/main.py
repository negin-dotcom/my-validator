from validator.validators import is_email


if __name__ == "__main__":
    assert is_email("negin@google.com") is True