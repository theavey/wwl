from functools import lru_cache
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from wordfreq import top_n_list


def get_static_dir() -> Path:
    # Project root is the parent of this file's directory
    return Path(__file__).resolve().parents[1] / "static"


@lru_cache(maxsize=1)
def load_five_letter_words() -> List[str]:
    # Pull a large English word list and filter to five-letter ASCII words
    words = top_n_list("en", n=1_000_000)
    filtered = {w.lower() for w in words if len(w) == 5 and w.isascii() and w.isalpha()}
    return sorted(filtered)


app = FastAPI(title="WWL - Word Filter")


# Serve static assets (CSS/JS) under /static
app.mount("/static", StaticFiles(directory=get_static_dir()), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(get_static_dir() / "index.html")


@app.get("/words.json", response_model=List[str])
def words_json() -> List[str]:
    return load_five_letter_words()
