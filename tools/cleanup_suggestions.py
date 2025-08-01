"""
cleanup_suggestions.py

Ein CLI-Tool zur Erkennung und optionalen Löschung potenziell überflüssiger Python-Dateien
(z. B. "test.py", "klasse1.py", "experiment_alt.py").

Funktionen:
- Erkennung verdächtiger Dateien basierend auf Dateinamen
- Filter nach Dateigröße (--min-size) und Alter (--min-age)
- Backup der zu löschenden Dateien in ZIP-Archiv (--backup)
- Automatisches Löschen ohne Nachfrage (--force)
- Berichte als Markdown und HTML

Beispiele:
    # Standardausführung (interaktiv mit Nachfragen)
    python cleanup_suggestions.py

    # Dateien vor dem Löschen sichern
    python cleanup_suggestions.py --backup

    # Automatisches Löschen (ohne Rückfrage), mit Backup
    python cleanup_suggestions.py --force --backup

    # Nur Dateien >2KB und älter als 7 Tage
    python cleanup_suggestions.py --min-size 2 --min-age 7
"""

import os
import argparse
import time
import zipfile
from datetime import datetime

# === Konfiguration ===

# Dateinamen, die auf verdächtige Dateien hinweisen
UNWANTED_KEYWORDS = [
    "test", "experiment", "alt", "demo", "sample",
    "tmp", "old", "backup", "klasse"
]

# Verzeichnisse, die ignoriert werden sollen
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "env", "venv", ".streamlit"}

# Nur auf diese Dateitypen prüfen
TARGET_EXTENSIONS = {".py"}

# Ausgabeberichte
REPORT_MD = "cleanup_report.md"
REPORT_HTML = "cleanup_report.html"

# Backup-Verzeichnis
BACKUP_DIR = ".backup"


# === Datei-Suche ===

def find_unwanted_files(project_root=".", min_size_kb=0, min_age_days=0):
    """
    Durchsucht das Projektverzeichnis nach potenziell überflüssigen Python-Dateien.

    :param project_root: Basisverzeichnis (default: aktuelles Verzeichnis)
    :param min_size_kb: Mindestgröße in Kilobyte
    :param min_age_days: Mindestalter in Tagen
    :return: Liste verdächtiger Dateipfade
    """
    suggestions = []
    now = time.time()
    min_age_secs = min_age_days * 86400  # Sekunden pro Tag

    for root, dirs, files in os.walk(project_root):
        # Unerwünschte Verzeichnisse ignorieren
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            # Nur .py-Dateien prüfen
            if not any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                continue

            # Nur Dateien mit verdächtigen Namen
            if not any(keyword in file.lower() for keyword in UNWANTED_KEYWORDS):
                continue

            file_path = os.path.join(root, file).replace("\\", "/").strip()
            size_kb = os.path.getsize(file_path) / 1024
            age_secs = now - os.path.getmtime(file_path)

            # Filter prüfen
            if size_kb >= min_size_kb and age_secs >= min_age_secs:
                suggestions.append(file_path)

    return suggestions


# === Backup ===

def create_backup(files):
    """
    Erstellt ein ZIP-Archiv aller Dateien, die gelöscht werden sollen.

    :param files: Liste der zu sichernden Dateien
    :return: Pfad zur ZIP-Datei
    """
    if not files:
        return None

    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    zip_name = f"backup_cleanup_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for f in files:
            try:
                # Nur relativen Pfad speichern, keine absoluten
                zipf.write(f, arcname=os.path.relpath(f, "."))
                print(f"📦 Gesichert: {f}")
            except Exception as e:
                print(f"⚠️  Fehler beim Sichern: {f} → {e}")

    return zip_path


# === Löschen ===

def delete_files(files, force=False):
    """
    Löscht die übergebenen Dateien – optional ohne Nachfrage.

    :param files: Liste der zu löschenden Dateien
    :param force: Wenn True, werden alle Dateien ohne Rückfrage gelöscht
    """
    for f in files:
        if not force:
            confirm = input(f"❓ Datei löschen: {f}? (j/n): ").strip().lower()
            if confirm != "j":
                print(f"⏭️ Übersprungen: {f}")
                continue
        try:
            os.remove(f)
            print(f"✅ Gelöscht: {f}")
        except Exception as e:
            print(f"❌ Fehler beim Löschen: {f} → {e}")


# === Berichte ===

def generate_markdown_report(file_list):
    """
    Erstellt einen Markdown-Bericht der gefundenen Dateien.
    """
    with open(REPORT_MD, "w", encoding="utf-8") as md:
        md.write("# 🧹 Cleanup-Vorschlag\n\n")
        if not file_list:
            md.write("✅ Keine verdächtigen Dateien gefunden.\n")
            return
        md.write("| Datei | Status |\n|-------|--------|\n")
        for f in file_list:
            md.write(f"| `{f}` | _Vorgeschlagen zur Löschung_ |\n")


def generate_html_report(file_list):
    """
    Erstellt einen HTML-Bericht der gefundenen Dateien.
    """
    with open(REPORT_HTML, "w", encoding="utf-8") as html:
        html.write("<html><head><meta charset='UTF-8'><title>Cleanup Report</title></head><body>")
        html.write("<h2>🧹 Cleanup-Vorschlag</h2>")
        if not file_list:
            html.write("<p><strong>Keine verdächtigen Dateien gefunden.</strong></p>")
        else:
            html.write("<table border='1'><tr><th>Datei</th><th>Status</th></tr>")
            for f in file_list:
                html.write(f"<tr><td>{f}</td><td>Vorgeschlagen zur Löschung</td></tr>")
            html.write("</table>")
        html.write("</body></html>")


# === Hauptprogramm ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup-Skript für unerwünschte Python-Dateien")
    parser.add_argument("--force", action="store_true", help="Alle Dateien ohne Rückfrage löschen")
    parser.add_argument("--backup", action="store_true", help="Dateien vor dem Löschen als ZIP sichern")
    parser.add_argument("--min-size", type=int, default=0, help="Nur Dateien größer als X KB einbeziehen")
    parser.add_argument("--min-age", type=int, default=0, help="Nur Dateien älter als X Tage einbeziehen")
    args = parser.parse_args()

    print("\n🔍 Starte Bereinigungsscanner...\n")

    unwanted_files = find_unwanted_files(
        project_root=".",
        min_size_kb=args.min_size,
        min_age_days=args.min_age
    )

    generate_markdown_report(unwanted_files)
    generate_html_report(unwanted_files)

    if unwanted_files:
        print("🚫 Verdächtige Dateien gefunden:\n")
        for f in unwanted_files:
            print(f"  - {f}")
        print("\n📄 Berichte gespeichert:")
        print(f" - Markdown: {REPORT_MD}")
        print(f" - HTML:     {REPORT_HTML}\n")

        if args.backup:
            print("📦 Starte Backup...\n")
            zip_result = create_backup(unwanted_files)
            print(f"\n🗂 Backup gespeichert unter: {zip_result}\n")

        delete_files(unwanted_files, force=args.force)
    else:
        print("✅ Keine verdächtigen Dateien gefunden.")