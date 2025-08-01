import csv
from typing import List, Dict
import os

def export_prompts_to_csv(prompts: List[Dict], file_path: str = "exported_prompts.csv") -> None:
    """
    Exportiert eine Liste von Prompts als CSV-Datei.

    :param prompts: Liste von Prompt-Dictionaries
    :param file_path: Pfad zur CSV-Datei
    """
    if not prompts:
        return

    keys = [
        "title", "category", "platform", "language",
        "purpose", "tags", "prompt", "notes", "last_modified"
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for p in prompts:
            row = {
                k: (", ".join(p[k]) if isinstance(p[k], list) else p.get(k, ""))
                for k in keys
            }
            writer.writerow(row)

def export_prompts_to_markdown(prompts: List[Dict], file_path: str = "exported_prompts.md") -> None:
    """
    Exportiert Prompts als Markdown-Datei.

    :param prompts: Liste von Prompts
    :param file_path: Pfad zur Markdown-Datei
    """
    with open(file_path, mode="w", encoding="utf-8") as f:
        for p in prompts:
            f.write(f"## {p.get('title', '-')}\n")
            f.write(f"**Kategorie:** {p.get('category', '-')}\n\n")
            f.write(f"**Plattform:** {p.get('platform', '-')}\n\n")
            f.write(f"**Sprache:** {p.get('language', '-')}\n\n")
            f.write(f"**Zweck:** {p.get('purpose', '-')}\n\n")
            f.write(f"**Tags:** {', '.join(p.get('tags', []))}\n\n")
            f.write(f"**Letzte Änderung:** {p.get('last_modified', '-')}\n\n")
            f.write(f"**Prompt:**\n\n{p.get('prompt', '-')}\n\n")
            f.write(f"**Notizen:**\n\n{p.get('notes', '-')}\n\n")
            f.write("---\n\n")
