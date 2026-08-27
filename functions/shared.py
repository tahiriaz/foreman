from functions import vars


def is_valid(value):
    if value is None:
        return False

    return (
        str(value).strip().upper()
        not in vars.INVALID_VALUES
    )
