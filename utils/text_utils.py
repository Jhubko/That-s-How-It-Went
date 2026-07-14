import re

def normalize_word(word):

    word = word.lower()

    word = word.replace(
        "'",
        ""
    )

    word = word.replace(
        "’",
        ""
    )

    word = re.sub(
        r"[^\w]",
        "",
        word
    )

    return word