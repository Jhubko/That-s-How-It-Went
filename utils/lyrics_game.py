from utils.text_utils import normalize_word


def create_missing_lyrics(lines, selected_line):

    result = []

    for line in lines:

        if line == selected_line:

            words = line["text"].split()

            hidden_words = []

            for word in words:

                clean_word = normalize_word(word)

                hidden_words.append(
                    "_" * len(clean_word)
                )

            result.append(
                " ".join(hidden_words)
            )

        else:

            result.append(
                line["text"]
            )

    return result