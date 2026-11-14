from validator.strings import all_of, is_str, min_length_of, max_length_of


name_valid = all_of(min_length_of(3), max_length_of(4), is_str)

if __name__ == "__main__":
    print(name_valid("you"))