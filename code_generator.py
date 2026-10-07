"""Brawl Stars team-code conversion and sequential generation helpers.

The conversion routines preserve the original project behavior for the website.
"""

import re

TEAM_CONVERSION_CHARS = "QWERTYUPASDFGHJKLZCVBNM23456789"
CONVERSION_CHARS = "0289PYLQGRJCUV"
TEAM_TAG = "X"
HASH_TAG = "#"


def to_long(hi_int, lo_int):
    return (hi_int << 32) | (lo_int & 0xFFFFFFFF)


def to_long_s(hi_int, lo_int):
    return (hi_int << 32) | lo_int


def convert(id_num, chars):
    result = ""
    length = len(chars)

    while id_num > 0:
        char_index = id_num % length
        result = chars[char_index] + result
        id_num -= char_index
        id_num //= length

    return result


def code_to_id(code):
    if not code or not code.startswith(TEAM_TAG):
        return -1

    code_substring = code[1:]
    if len(code_substring) < 1:
        return 0

    unk6 = 0
    unk7 = 0

    for char in code_substring:
        sub_str_idx = TEAM_CONVERSION_CHARS.find(char)

        if sub_str_idx <= -1:
            return -1

        unk12 = unk6 * len(TEAM_CONVERSION_CHARS) + sub_str_idx
        unk7 = (
            to_long(unk7, unk6) * len(TEAM_CONVERSION_CHARS) + sub_str_idx
        ) >> 32
        unk6 = unk12

    if (unk6 & unk7) != -1:
        v13 = to_long_s(unk7, unk6) >> 8
        lo_int = v13 & 0x7FFFFFFF
        hi_int = unk6 & 0xFF
        return to_long(hi_int, lo_int)

    return -1


def id_to_code(id_num):
    hi_int = (id_num >> 32) & 0xFFFFFFFF
    lo_int = id_num & 0xFFFFFFFF

    if hi_int < 256:
        value = to_long((lo_int >> 24), hi_int | (lo_int << 8))
        return TEAM_TAG + convert(value, TEAM_CONVERSION_CHARS)

    return None


def generate_hash_code(id_num):
    hi_int = id_num >> 32
    lo_int = id_num & 0xFFFFFFFF

    if hi_int < 256:
        value = to_long((lo_int >> 24), hi_int | (lo_int << 8))
        return HASH_TAG + convert(value, CONVERSION_CHARS)

    return None


def is_valid_team_code(code):
    if not code:
        return False

    code = code.strip().upper()

    return (
        code.startswith(TEAM_TAG)
        and 2 <= len(code) <= 9
        and all(char in TEAM_CONVERSION_CHARS for char in code[1:])
    )


def extract_team_code_from_link(text):
    match = re.search(r"tag=([A-Za-z0-9]+)", text or "")
    if match:
        code = match.group(1).upper()
        if is_valid_team_code(code):
            return code
    return None


def parse_team_code(text):
    """Accept either a team code or an invite URL containing its tag."""
    if not isinstance(text, str):
        return None

    text = text.strip()
    return extract_team_code_from_link(text) or text.upper()


def generate_sequential_codes(base_code, offset=0, count=10):
    numeric_id = code_to_id(base_code)
    if numeric_id == -1:
        raise ValueError("Invalid team code")

    base_id_with_offset = numeric_id + offset
    codes = []

    for index in range(count):
        current_id = base_id_with_offset + index
        new_team_code = id_to_code(current_id)
        hash_code = generate_hash_code(current_id)

        if new_team_code and hash_code:
            codes.append(
                {
                    "team_code": new_team_code,
                    "hash_code": hash_code,
                }
            )

    return codes
