"""
PromptRepository – Datenzugriffsschicht für AI-Prompt-Verwaltung mit TinyDB.

Diese Klasse kapselt alle Interaktionen mit der Datenbank (TinyDB) und stellt
Methoden zum Einfügen, Suchen, Aktualisieren und Löschen von Prompts bereit.
"""

from tinydb import TinyDB, Query
from datetime import datetime
from typing import List, Optional, Dict
from utils.logger import configure_logger
logger = configure_logger(__name__)


class PromptRepository:
    """
    Repository-Klasse für die Verwaltung von AI-Prompts in einer TinyDB-Datenbank.
    """

    def __init__(self, db_path: str = "database.json"):
        """
        Initialisiert die Datenbankverbindung.

        :param db_path: Pfad zur JSON-Datenbankdatei.
        """
        self.db = TinyDB(db_path)
        self.query = Query()

    def close(self):
        self.db.close()

    def add_prompt(self, title: str, category: str, platform: str,
               tags: List[str], prompt_text: str,
               language: str = "", purpose: str = "", notes: str = "") -> int:
        return self.db.insert({
            "title": title,
            "category": category,
            "platform": platform,
            "tags": tags,
            "prompt": prompt_text,
            "language": language,
            "purpose": purpose,
            "notes": notes,
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def get_all_prompts(self) -> List[Dict]:
        """
        Gibt alle gespeicherten Prompts zurück.

        :return: Liste aller Prompt-Datensätze.
        """
        return self.db.all()

    def search_prompts(self, keyword: str = "", category: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> List[Dict]:
        """
        Durchsucht die Datenbank nach Prompts anhand von Stichwort, Kategorie und Tags.

        :param keyword: Suchbegriff im Titel oder Prompt-Text.
        :param category: (Optional) Kategorie-Filter.
        :param tags: (Optional) Liste von Tags zur Filterung.
        :return: Gefilterte Liste von Prompts.
        """
        results = self.db.all()

        if keyword:
            keyword_lower = keyword.lower()
            results = [p for p in results
                       if keyword_lower in p.get("title", "").lower()
                       or keyword_lower in p.get("prompt", "").lower()]

        if category:
            results = [p for p in results if p.get("category") == category]

        if tags:
            results = [p for p in results if any(tag in p.get("tags", []) for tag in tags)]

        return results

    def update_prompt(self, doc_id: int, updated_data: Dict) -> None:
        """
        Aktualisiert einen bestehenden Prompt.

        :param doc_id: ID des zu aktualisierenden Prompts.
        :param updated_data: Wörterbuch mit zu aktualisierenden Feldern.
        """
        updated_data["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("Aktualisierte Daten: %s", updated_data)
        self.db.update(updated_data, doc_ids=[doc_id])

    def delete_prompt(self, doc_id: int) -> None:
        """
        Entfernt einen Prompt aus der Datenbank.

        :param doc_id: ID des zu löschenden Prompts.
        """
        logger.debug("Prompt geloescht (ID): %d", doc_id)
        self.db.remove(doc_ids=[doc_id])

    def get_all_categories(self) -> List[str]:
        """
        Gibt eine alphabetisch sortierte Liste aller eindeutigen Kategorien zurück.

        :return: Liste der Kategorien.
        """
        prompts = self.db.all()
        logger.debug("Liste Aller Kategorien ermittelt")
        return sorted(set(p.get("category", "") for p in prompts if p.get("category")))

    def get_all_tags(self) -> List[str]:
        """
        Gibt eine alphabetisch sortierte Liste aller verwendeten Tags zurück.

        :return: Liste der Tags.
        """
        prompts = self.db.all()
        all_tags = []
        for p in prompts:
            tags = p.get("tags", [])
            if isinstance(tags, list):
                all_tags.extend(tags)
        return sorted(set(all_tags))




