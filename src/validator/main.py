from validator.strings import all_of


def spy(result, calls):
    def check(value):
        calls.append(value)
        return result 

    return check


if __name__ == "__main__":
    calls = []
    v = all_of(spy(False, calls), spy(True, calls))
    result = v("hyey")
    print(result)