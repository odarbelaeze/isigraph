"""Utility functions for graph loading.

There are some graphs, then we load them.
"""


import wostools

from isigraph.store import add_articles


def prepend(text: str, prefix: str):
    """Prepend a prefix to a string if the string exists.
    """
    if not text:
        return text
    return prefix + text


def get_label_for(article: wostools.Article):
    """Get a label for an article, this is what a citation's going to be.
    """
    author = article._data.get('AU', [''])[0].replace(',', '')
    year = article._data.get('PY', [''])[0]
    journal = article._data.get('J9', [''])[0]
    parts = [author, year, journal]
    volume = prepend(article._data.get('VL', [''])[0], 'V')
    if volume:
        parts.append(volume)
    page = prepend(article._data.get('BP', [''])[0], 'P')
    if page:
        parts.append(page)
    doi = prepend(article._data.get('DI', [''])[0], 'DOI ')
    if doi:
        parts.append(doi)
    return ', '.join(parts)


def read_files(filenames: list):
    collection = wostools.CollectionLazy(*filenames)
    for article in collection.articles:
        label = get_label_for(article)
        yield label, article


def store(filenames: list):
    add_articles(read_files(filenames), 'bolt://localhost:7687')
