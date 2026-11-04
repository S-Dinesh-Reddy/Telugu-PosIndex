import os
import json
import sqlite3

from dataset_loader import load_wikipedia_articles
from text_processor import tokenize


def build_index(articles, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS postings")
    cursor.execute("DROP TABLE IF EXISTS vocabulary")
    cursor.execute("DROP TABLE IF EXISTS documents")

    cursor.execute("""
        CREATE TABLE documents (
            doc_id TEXT PRIMARY KEY,
            title TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE postings (
            term TEXT,
            doc_id TEXT,
            positions TEXT,
            PRIMARY KEY (term, doc_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE vocabulary (
            term TEXT PRIMARY KEY,
            cf INTEGER,
            df INTEGER
        )
    """)

    vocabulary = {}
    document_count = 0

    for article in articles:
        doc_id = article["doc_id"]
        title = article["title"]
        words = tokenize(article["text"])

        positions = {}

        for position, word in enumerate(words):
            if word not in positions:
                positions[word] = []

            positions[word].append(position)

        cursor.execute(
            "INSERT INTO documents VALUES (?, ?)",
            (doc_id, title)
        )

        for word, word_positions in positions.items():
            cursor.execute(
                "INSERT INTO postings VALUES (?, ?, ?)",
                (word, doc_id, json.dumps(word_positions))
            )

            if word not in vocabulary:
                vocabulary[word] = {"cf": 0, "df": 0}

            vocabulary[word]["cf"] += len(word_positions)
            vocabulary[word]["df"] += 1

        document_count += 1

        if document_count % 100 == 0:
            conn.commit()

    for word, stats in vocabulary.items():
        cursor.execute(
            "INSERT INTO vocabulary VALUES (?, ?, ?)",
            (word, stats["cf"], stats["df"])
        )

    cursor.execute("CREATE INDEX posting_term_index ON postings(term)")

    conn.commit()
    conn.close()

    print(f"Indexed {document_count} documents.")
    print(f"Vocabulary size: {len(vocabulary)}")


if __name__ == "__main__":
    dataset_path = "data/raw/tewiki-latest-pages-articles.xml.bz2"
    db_path = "index/positional_index.db"

    articles = load_wikipedia_articles(dataset_path, max_articles=5)

    build_index(articles, db_path)