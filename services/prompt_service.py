"""
PromptService – Geschäftslogik zur Verwaltung und Verarbeitung von AI-Prompts.

Diese Schicht kapselt die logische Verarbeitung und Validierung von Prompts,
unabhängig von UI oder Datenbankimplementierung.
"""

from typing import List, Optional, Dict
from models.prompt_model import PromptRepository
from utils.logger import configure_logger


logger = configure_logger(__name__)

class PromptService:
    """
    Service-Klasse zur zentralen Steuerung von Prompt-bezogenen Operationen.
    """

    def __init__(self, repository: Optional[PromptRepository] = None):
        """
        Initialisiert den Service mit einer PromptRepository-Instanz.

        :param repository: Optionale Repository-Instanz (für Tests/Mocking).
        """
        self.repo = repository or PromptRepository()

    def create_prompt(self, title: str, category: str, platform: str,
                  tags: List[str], prompt_text: str,
                  language: str = "", purpose: str = "", notes: str = "") -> int:
        """
        Validiert und erstellt einen neuen Prompt.

        :return: Dokument-ID des gespeicherten Prompts.
        :raises ValueError: Bei ungültigen Eingaben.
        """
        logger.info("Neuer Prompt erstellt: %s", title)
        
        if not title.strip():
            logger.error("Titel darf nicht leer sein.")
            raise ValueError("Titel darf nicht leer sein.")
        if not prompt_text.strip():
            logger.error("Titel darf nicht leer sein.")
            raise ValueError("Prompt-Text darf nicht leer sein.")
        return self.repo.add_prompt(title, category, platform, tags, prompt_text, language, purpose, notes)

    def get_all_prompts(self) -> List[Dict]:
        """Gibt alle gespeicherten Prompts zurück."""
        return self.repo.get_all_prompts()

    def search_prompts(self, keyword: str = "", category: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> List[Dict]:
        """Sucht nach Prompts anhand von Stichwort, Kategorie und Tags."""
        return self.repo.search_prompts(keyword, category, tags)

    def update_prompt(self, doc_id: int, updated_data: Dict) -> None:
        """Aktualisiert einen bestehenden Prompt."""
        if "title" in updated_data and not updated_data["title"].strip():
            logger.error("Titel darf nicht leer sein.")
            raise ValueError("Titel darf nicht leer sein.")
        if "prompt" in updated_data and not updated_data["prompt"].strip():
            logger.error("Prompt-Text darf nicht leer sein.")
            raise ValueError("Prompt-Text darf nicht leer sein.")
        self.repo.update_prompt(doc_id, updated_data)

    def delete_prompt(self, doc_id: int) -> None:
        """Löscht einen Prompt anhand der Dokument-ID."""
        self.repo.delete_prompt(doc_id)

    def get_all_categories(self) -> List[str]:
        """Gibt alle eindeutigen Kategorien zurück."""
        return self.repo.get_all_categories()

    def get_all_tags(self) -> List[str]:
        """Gibt alle eindeutigen Tags zurück."""
        return self.repo.get_all_tags()
