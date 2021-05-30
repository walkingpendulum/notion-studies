import os
import subprocess
import tempfile


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


def render_dot(content: str, output_picture_name: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".dot", prefix="graph_", mode="w", delete=False) as temp_obj:
        temp_obj.write(content)

    try:
        subprocess.run(["dot", "-Tpng", temp_obj.name, "-o", output_picture_name], check=True)
    finally:
        try:
            os.unlink(temp_obj.name)
        except Exception:
            pass