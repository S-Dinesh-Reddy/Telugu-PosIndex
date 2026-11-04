
import os
import sqlite3

from search import search_term, search_phrase


DB_PATH = "index/positional_index.db"
OUTPUT_PATH = "output/telugu_output.txt"

MAX_EXAMPLES_PER_TEST = 3
NUMBER_OF_RARE_TERMS = 10
INDEXED_DOCUMENTS = 9000


def write_term_result(file, query):
    result = search_term(query, DB_PATH)

    if not result:
        file.write("No results found.\n")
        return

    file.write(f"Collection Frequency (CF): {result['cf']}\n")
    file.write(f"Document Frequency (DF): {result['df']}\n")

    postings = result["postings"]

    file.write(
        f"\nShowing {min(len(postings), MAX_EXAMPLES_PER_TEST)} "
        f"of {len(postings)} matching documents:\n"
    )

    for posting in postings[:MAX_EXAMPLES_PER_TEST]:
        file.write(f"\nDocument: {posting['title']}\n")
        file.write(f"Document ID: {posting['doc_id']}\n")
        file.write(f"Positions: {posting['positions']}\n")


def write_phrase_result(file, query):
    results = search_phrase(query, DB_PATH)

    if not results:
        file.write("No phrase matches found.\n")
        return

    file.write(f"Total phrase occurrences: {len(results)}\n")
    file.write(
        f"\nShowing {min(len(results), MAX_EXAMPLES_PER_TEST)} "
        f"of {len(results)} phrase occurrences:\n"
    )

    for match in results[:MAX_EXAMPLES_PER_TEST]:
        file.write(f"\nDocument: {match['title']}\n")
        file.write(f"Document ID: {match['doc_id']}\n")
        file.write(f"Starting position: {match['start_position']}\n")


def get_rare_terms():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT term, cf, df
        FROM vocabulary
        WHERE df BETWEEN 2 AND 9
        ORDER BY df ASC, cf ASC, term ASC
    """)

    candidates = cursor.fetchall()
    connection.close()

    candidates = [
        item for item in candidates
        if 3 <= len(item[0]) <= 15
        and any(
            "\u0C00" <= character <= "\u0C7F"
            for character in item[0]
        )
    ]

    if len(candidates) < NUMBER_OF_RARE_TERMS:
        print(
            f"Only {len(candidates)} rare terms found. "
            "Cannot provide 10 terms."
        )
        return candidates

    step = len(candidates) / NUMBER_OF_RARE_TERMS

    selected = [
        candidates[int(index * step)]
        for index in range(NUMBER_OF_RARE_TERMS)
    ]

    return selected


def write_rare_terms(file):
    file.write("\n" + "=" * 60 + "\n")
    file.write("10 RARE TERMS WITH THEIR POSITIONAL INDEX\n")
    file.write("=" * 60 + "\n")

    terms = get_rare_terms()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for number, (term, cf, df) in enumerate(terms, start=1):
        file.write(f"\n{number}. Term: {term}\n")
        file.write(f"Collection Frequency (CF): {cf}\n")
        file.write(f"Document Frequency (DF): {df}\n")
        file.write("  Positional index:\n")

        cursor.execute("""
            SELECT p.doc_id, d.title, p.positions
            FROM postings p
            JOIN documents d ON p.doc_id = d.doc_id
            WHERE p.term = ?
            ORDER BY p.doc_id
        """, (term,))

        rows = cursor.fetchall()

        for doc_id, title, positions in rows:
            file.write(f"    Document: {title}\n")
            file.write(f"    Document ID: {doc_id}\n")
            file.write(f"    Positions: {positions}\n")

    connection.close()


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    test_cases = [
        ("గోదావరి", "Term"),
        ("తెలుగు", "Term"),
        ("భారతదేశం", "Term"),
        ("తెలుగు భాష", "Phrase"),
        ("తెలుగు సాహిత్యం", "Phrase"),
    ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write("POSITIONAL INDEX SEARCH RESULTS\n")
        file.write("Dataset: Telugu Wikipedia\n")
        file.write(f"Indexed documents: {INDEXED_DOCUMENTS}\n")
        file.write("\n5 SEARCH TEST CASES\n")

        for number, (query, query_type) in enumerate(test_cases, start=1):
            file.write("\n" + "=" * 60 + "\n")
            file.write(f"TEST CASE {number}\n")
            file.write(f"Query: {query}\n")
            file.write(f"Type: {query_type}\n")
            file.write("=" * 60 + "\n")

            if query_type == "Term":
                write_term_result(file, query)
            else:
                write_phrase_result(file, query)

        write_rare_terms(file)

    print(f"Output generated successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
