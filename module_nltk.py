#!/usr/bin/env python3
import nltk
from nltk.tokenize import sent_tokenize

# Download the Punkt models once at import time
nltk.download('punkt', quiet=True)

def curate_text(text: str) -> str:
    """
    Split `text` into sentences using NLTK’s Punkt tokenizer
    and rejoin with single spaces.
    """
    sentences = sent_tokenize(text)
    return ' '.join(sentences)
