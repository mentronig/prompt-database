# utils/backup.py
import shutil
import os
from datetime import datetime

def backup_database(source_path="database.json", backup_dir="backups") -> str:
    """
    Erstellt eine zeitgestempelte Kopie der JSON-Datenbank im Backup-Verzeichnis.

    :param source_path: Pfad zur Originaldatenbank
    :param backup_dir: Zielverzeichnis für Backups
    :return: Pfad zur erstellten Backup-Datei
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.json")
    shutil.copy2(source_path, backup_file)
    return backup_file



