
from dataset_loader import load_wikipedia_articles
from positional_index import build_index
from search import search_term, search_phrase


DATASET_PATH = "data/raw/tewiki-latest-pages-articles.xml.bz2"
DB_PATH = "index/positional_index.db"


def build():
    amount = input(
        "How many articles should be indexed? "
        "(Press Enter for default 100): "
    ).strip()

    if amount:
        max_articles = int(amount)
    else:
        max_articles = 100

    articles = load_wikipedia_articles(
        DATASET_PATH,
        max_articles=max_articles
    )

    build_index(articles, DB_PATH)


def search_word():
    term = input("Enter a Telugu word: ").strip()
    result = search_term(term, DB_PATH)

    if result is None:
        print("\nTerm not found in the index.")
        return

    print(f"\nTerm: {result['term']}")
    print(f"Collection Frequency (CF): {result['cf']}")
    print(f"Document Frequency (DF): {result['df']}")

    for posting in result["postings"]:
        print(f"\nDocument: {posting['title']}")
        print(f"Document ID: {posting['doc_id']}")
        print(f"Positions: {posting['positions']}")


def search_for_phrase():
    phrase = input("Enter a Telugu phrase: ").strip()
    results = search_phrase(phrase, DB_PATH)

    print("\nPhrase matches:")

    if not results:
        print("No matching phrase found.")
        return

    for result in results:
        print(f"\nDocument: {result['title']}")
        print(f"Document ID: {result['doc_id']}")
        print(f"Starting position: {result['start_position']}")


def main():
    while True:
        print("\n===== Telugu-PosIndex: Telugu Positional Search =====")
        print("1. Build positional index")
        print("2. Search for a word")
        print("3. Search for a phrase")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            build()
        elif choice == "2":
            search_word()
        elif choice == "3":
            search_for_phrase()
        elif choice == "4":
            print("Exiting Telugu-PosIndex.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
