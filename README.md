# WWL - Five-Letter Words Filter

A tiny FastAPI app that serves a single-page site listing all English five-letter words in alphabetical order. Enter letters to exclude, and any word containing those letters disappears from the list. Words render in a fixed-width font.

## Requirements

- [pixi](https://pixi.sh) (Conda-based project/environment manager)

## Setup

```bash
pixi install
```

## Run the server

```bash
pixi run serve
```

Then open `http://127.0.0.1:8000` in your browser.

## Project layout

- `app/main.py`: FastAPI application and endpoints
- `static/index.html`: Frontend markup, styles, and filtering logic
- `pixi.toml`: Environment specification and tasks

## Implementation notes

- The word list is derived at runtime using NLTK's WordNet lexical database, extracting unique words from synsets and filtering to five-letter ASCII alphabetic words. This provides a comprehensive dictionary without invalid entries like repeated letters, with more words than the basic word corpus. The result is cached in-process for speed.
- The frontend fetches `/words.json` once and filters purely client-side for instant interactions.

