from neo4j.v1 import GraphDatabase


ADD_ARTICLE = """
MERGE (a:Article {label: $label})
SET a = $data
"""

ADD_CITATION = """
MERGE (a:Article {label: $citer})
MERGE (a)-[:CITES]->(b:Article {label: $citee})
"""


def add_article(tx: 'transaction', label: str, data: dict):
    """Store an article in the database, merge style.
    """
    tx.run(ADD_ARTICLE, label=label, data={'label': label, **data})

def add_citation(tx: 'transaction', citer: str, citee: str):
    """Store a citation in the database, merge style.
    """
    tx.run(ADD_CITATION, citer=citer, citee=citee)


def add_articles(iterator, host: str):
    driver = GraphDatabase.driver(host)
    with driver.session() as session:
        for label, article in iterator:
            print(label)
            session.write_transaction(add_article, label, article._data)
            for citation in article._data.get('CR', []):
                session.write_transaction(add_citation, label, citation.strip())
