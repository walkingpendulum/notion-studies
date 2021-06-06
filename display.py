def split_long_sentences(sentence, chars_per_line=15):
    sentence = sentence.strip()
    if len(sentence) <= chars_per_line:
        return sentence

    words = sentence.split(' ')
    line, length = [], 0
    for word in words:
        if length > chars_per_line:
            result = f'{" ".join(line)}\\n{split_long_sentences(sentence[length:])}'
            return result

        line.append(word)
        length += len(word) + 1  # spaces

    return " ".join(line)
