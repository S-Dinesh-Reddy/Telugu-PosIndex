import json
import sqlite3

from text_processor import tokenize


def search_term(term, db_path="index/positional_index.db"):
    words = tokenize(term)

    if len(words) != 1:
        return None

    term = words[0]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = cursor.execute(
        "SELECT cf, df FROM vocabulary WHERE term = ?",
        (term,)
    ).fetchone()

    if result is None:
        conn.close()
        return None

    cf, df = result

    rows = cursor.execute(
        """
        SELECT documents.doc_id, documents.title, postings.positions
        FROM postings
        JOIN documents ON postings.doc_id = documents.doc_id
        WHERE postings.term = ?
        ORDER BY documents.doc_id
        """,
        (term,)
    ).fetchall()

    conn.close()

    postings = []

    for doc_id, title, positions in rows:
        postings.append({
            "doc_id": doc_id,
            "title": title,
            "positions": json.loads(positions)
        })

    return {
        "term": term,
        "cf": cf,
        "df": df,
        "postings": postings
    }


def search_phrase(phrase, db_path="index/positional_index.db"):
    words = tokenize(phrase)

    if not words:
        return []

    term_results = []

    for word in words:
        result = search_term(word, db_path)

        if result is None:
            return []

        term_results.append({
            posting["doc_id"]: {
                "title": posting["title"],
                "positions": set(posting["positions"])
            }
            for posting in result["postings"]
        })

    common_documents = set(term_results[0])

    for result in term_results[1:]:
        common_documents &= set(result)

    matches = []

    for doc_id in common_documents:
        first_positions = term_results[0][doc_id]["positions"]
        title = term_results[0][doc_id]["title"]

        for position in sorted(first_positions):
            found = True

            for i in range(1, len(words)):
                next_positions = term_results[i][doc_id]["positions"]

                if position + i not in next_positions:
                    found = False
                    break

            if found:
                matches.append({
                    "doc_id": doc_id,
                    "title": title,
                    "start_position": position
                })

    matches.sort(key=lambda match: (match["doc_id"], match["start_position"]))

    return matches


if __name__ == "__main__":
    term = input("Enter a Telugu word: ").strip()
    result = search_term(term)

    if result is None:
        print("Term not found.")
    else:
        print(f"\nTerm: {result['term']}")
        print(f"CF: {result['cf']}")
        print(f"DF: {result['df']}")

        for posting in result["postings"]:
            print(f"\nDocument: {posting['title']}")
            print(f"Document ID: {posting['doc_id']}")
            print(f"Positions: {posting['positions']}")

    phrase = input("\nEnter a Telugu phrase: ").strip()
    phrase_results = search_phrase(phrase)

    print("\nPhrase matches:")

    for match in phrase_results:
        print(
            f"Document: {match['title']}, "
            f"Document ID: {match['doc_id']}, "
            f"Starting position: {match['start_position']}"
        )