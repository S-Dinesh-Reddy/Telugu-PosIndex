import os
import sys
import tempfile
import unittest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from positional_index import build_index
from search import search_term, search_phrase


class TestPositionalIndex(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name,
            "test_index.db"
        )

        articles = [
            {
                "doc_id": "1",
                "title": "డాక్ 1",
                "text": "తెలుగు భాష తెలుగు రాష్ట్రం"
            },
            {
                "doc_id": "2",
                "title": "డాక్ 2",
                "text": "తెలుగు రాష్ట్రం తెలుగు"
            }
        ]

        build_index(articles, self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_collection_and_document_frequency(self):
        result = search_term("తెలుగు", self.db_path)

        self.assertIsNotNone(result)
        self.assertEqual(result["cf"], 4)
        self.assertEqual(result["df"], 2)

    def test_term_positions(self):
        result = search_term("తెలుగు", self.db_path)

        first_document = next(
            posting for posting in result["postings"]
            if posting["doc_id"] == "1"
        )

        self.assertEqual(first_document["positions"], [0, 2])

    def test_phrase_search(self):
        results = search_phrase("తెలుగు భాష", self.db_path)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["doc_id"], "1")
        self.assertEqual(results[0]["start_position"], 0)

    def test_nonexistent_phrase(self):
        results = search_phrase("భాష రాష్ట్రం తెలుగు", self.db_path)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()