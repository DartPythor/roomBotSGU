import string


async def is_valid_digit(number) -> bool:
    for i in number:
        if i not in string.digits:
            return False
    return True
