import re
import unicodedata


def clean_text(text):
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\{\{.*?\}\}", " ", text, flags=re.DOTALL)
    text = re.sub(r"\[\[([^|\]]*\|)?([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"'{2,}", "", text)
    text = re.sub(r"={2,}", " ", text)
    text = re.sub(r"[\|{}\[\]*#]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    text = clean_text(text)

    candidates = re.findall(r"[\u0C00-\u0C7F]+", text)

    words = []

    for word in candidates:
        if unicodedata.category(word[0]).startswith("L"):
            words.append(word)

    return words


if __name__ == "__main__":
    sample = """
    {{Infobox}}
    '''[[ఆంధ్రప్రదేశ్|ఆంధ్రప్రదేశ్]]''' ఒక [[రాష్ట్రం]].
    <div>తెలుగు భాష</div>
    """

    print(clean_text(sample))
    print(tokenize(sample))