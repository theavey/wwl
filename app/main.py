from functools import lru_cache
from pathlib import Path

import nltk
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from nltk.corpus import wordnet


def get_static_dir() -> Path:
    # Project root is the parent of this file's directory
    return Path(__file__).resolve().parents[1] / "static"


@lru_cache(maxsize=1)
def load_five_letter_words() -> list[str]:
    # Download NLTK wordnet corpus if not already present
    try:
        nltk.data.find("corpora/wordnet.zip")
    except LookupError:
        nltk.download("wordnet", quiet=True)

    # Use clean English word list from WordNet and filter to five-letter words
    # Extract unique lemma names (words) from all synsets
    wordnet_words = set()
    for synset in wordnet.all_synsets():
        for lemma in synset.lemmas():
            wordnet_words.add(lemma.name())

    filtered = {
        w.lower() for w in wordnet_words if len(w) == 5 and w.isascii() and w.isalpha()
    }
    return sorted(filtered)


app = FastAPI(title="WWL - Word Filter")


# Serve static assets (CSS/JS) under /static
app.mount("/static", StaticFiles(directory=get_static_dir()), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(get_static_dir() / "index.html")


@app.get("/words.json", response_model=list[str])
def words_json() -> list[str]:
    return load_five_letter_words()
