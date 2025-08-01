import unittest
import os
from models.prompt_model import PromptRepository

TEST_DB_PATH = "test_database.json"

class TestPromptRepository(unittest.TestCase):
    def setUp(self):
        self.repo = PromptRepository(TEST_DB_PATH)
        self.repo.db.truncate()  # Leeren vor jedem Test

    def tearDown(self):
        try:
            if hasattr(self.repo, "db"):
                self.repo.close()
        finally:
            if os.path.exists(TEST_DB_PATH):
                os.remove(TEST_DB_PATH)

    def test_add_and_get_prompt(self):
        """Prompt speichern und wieder abrufen"""
        doc_id = self.repo.add_prompt(
            title="Testprompt",
            category="Test",
            platform="ChatGPT",
            tags=["test"],
            prompt_text="Dies ist ein Test.",
            language="Deutsch",
            purpose="UnitTest",
            notes="Keine"
        )
        all_prompts = self.repo.get_all_prompts()
        self.assertEqual(len(all_prompts), 1)
        self.assertEqual(all_prompts[0]["title"], "Testprompt")

    def test_search_by_tag(self):
        """Prompt suche nach Tag"""
        self.repo.add_prompt("T1", "A", "ChatGPT", ["alpha"], "p", "de", "p", "")
        self.repo.add_prompt("T2", "B", "Claude", ["beta"], "p", "de", "p", "")
        results = self.repo.search_prompts(tags=["alpha"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "T1")


if __name__ == "__main__":
    unittest.main()