
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)

def curate_text(text: str) -> str:

    sentences = sent_tokenize(text)
    return ' '.join(sentences)
