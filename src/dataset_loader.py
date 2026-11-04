import bz2
from lxml import etree


def load_wikipedia_articles(file_path, max_articles=5000):
    namespace = "{http://www.mediawiki.org/xml/export-0.11/}"

    with bz2.open(file_path, "rb") as file:
        context = etree.iterparse(file, events=("end",), tag=f"{namespace}page")

        article_count = 0

        for _, page in context:
            title = page.findtext(f"{namespace}title")
            page_id = page.findtext(f"{namespace}id")
            namespace_id = page.findtext(f"{namespace}ns")
            text = page.findtext(f".//{namespace}revision/{namespace}text")

            if namespace_id == "0" and text and title:
                if page.find(f"{namespace}redirect") is None:
                    yield {
                        "doc_id": page_id,
                        "title": title,
                        "text": text
                    }

                    article_count += 1

                    if article_count >= max_articles:
                        break

            page.clear()

    print(f"Loaded {article_count} articles.")


if __name__ == "__main__":
    dataset_path = "data/raw/tewiki-latest-pages-articles.xml.bz2"

    for article in load_wikipedia_articles(dataset_path, max_articles=5):
        print(f"\nTitle: {article['title']}")
        print(f"Document ID: {article['doc_id']}")
        print(f"Text preview: {article['text'][:100]}")