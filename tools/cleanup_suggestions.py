"""
cleanup_suggestions.py

Cleanup-Tool zur Erkennung und optionalen Löschung überflüssiger Python-Dateien.
Version 0.8 – mit Logging & Dry-Run-Modus

Autor: Roland + Alisa (AI)
Stand: 2025-08-01

Funktionen:
- Erkennung verdächtiger .py-Dateien anhand von Namen (test, tmp, klasse etc.)
- Filterung nach Mindestgröße (--min-size) und Alter (--min-age)
- Optionales ZIP-Backup vor Löschung (--backup)
- Optionaler Dry-Run (Simulationsmodus ohne Änderungen)
- Logging aller Aktionen in cleanup.log
- Berichte in Markdown und HTML


## ⚙️ Beispielaufrufe


# Interaktiver Modus (Standard)
python tools/cleanup_suggestions.py

# Nur Dateien über 2 KB und älter als 7 Tage
python tools/cleanup_suggestions.py --min-size 2 --min-age 7

# Alles automatisch löschen mit Backup
python tools/cleanup_suggestions.py --force --backup

# Nur anzeigen, was gelöscht würde (Simulation)
python tools/cleanup_suggestions.py --dry-run

# Kombination: Backup + direktes Löschen + Filter
python tools/cleanup_suggestions.py --force --backup --min-size 3 --min-age 14
"""

import os
import argparse
import time
import zipfile
import logging
from datetime import datetime

# === Konfiguration ===

UNWANTED_KEYWORDS = [
    "test", "experiment", "alt", "demo", "sample", "tmp", "old", "backup", "klasse"
]
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "env", "venv", ".streamlit"}
TARGET_EXTENSIONS = {".py"}

REPORT_MD = "cleanup_report.md"
REPORT_HTML = "cleanup_report.html"
BACKUP_DIR = ".backup"
LOG_FILE = "cleanup.log"

# === Logging Setup ===

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

PROTECTED_PATHS = [
    "tests/test_prompt_repository.py",
    "utils/backup.py"
]

def is_protected(path):
    return any(path.endswith(p) or path.replace("\\", "/").endswith(p) for p in PROTECTED_PATHS)


# === Datei-Suche ===

def find_unwanted_files(project_root=".", min_size_kb=0, min_age_days=0):
    """
    Scannt das Projekt nach verdächtigen .py-Dateien basierend auf:
    - Namen mit bestimmten Schlüsselwörtern
    - Größe und Alter

    Rückgabe: Liste der verdächtigen Dateipfade
    """
    suggestions = []
    now = time.time()
    min_age_secs = min_age_days * 86400

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if not any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                continue
            if not any(keyword in file.lower() for keyword in UNWANTED_KEYWORDS):
                continue

            file_path = os.path.join(root, file).replace("\\", "/").strip()
            size_kb = os.path.getsize(file_path) / 1024
            age_secs = now - os.path.getmtime(file_path)

            if size_kb >= min_size_kb and age_secs >= min_age_secs:
                suggestions.append(file_path)
                logging.info(f"Datei zur Löschung vorgeschlagen: {file_path}")
    return suggestions

# === Backup ===

def create_backup(files):
    """
    Erstellt ein ZIP-Archiv aller zu löschenden Dateien.

    Rückgabe: Pfad zur ZIP-Datei
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
                zipf.write(f, arcname=os.path.relpath(f, "."))
                logging.info(f"Backup gespeichert: {f}")
            except Exception as e:
                logging.error(f"Fehler beim Backup: {f} → {e}")
    return zip_path

# === Löschung ===

def delete_files(files, force=False, dry_run=False):
    for f in files:
        if is_protected(f):
            print(f"⛔ Geschützte Datei übersprungen: {f}")
            logging.info(f"⛔ Geschützte Datei übersprungen: {f}")
            continue

        if dry_run:
            print(f"[Dry-Run] 🔎 Datei wäre gelöscht worden: {f}")
            logging.info(f"[Dry-Run] Datei markiert zur Löschung: {f}")
            continue

        if not force:
            confirm = input(f"❓ Datei löschen: {f}? (j/n): ").strip().lower()
            if confirm != "j":
                print(f"⏭️ Übersprungen: {f}")
                logging.info(f"Benutzer übersprang Datei: {f}")
                continue

        try:
            os.remove(f)
            print(f"✅ Gelöscht: {f}")
            logging.info(f"Datei gelöscht: {f}")
        except Exception as e:
            print(f"❌ Fehler beim Löschen: {f} → {e}")
            logging.error(f"Fehler beim Löschen: {f} → {e}")

# === Berichte ===

def generate_markdown_report(file_list):
    """
    Erstellt einen Markdown-Bericht zur Übersicht.
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
    Erstellt einen HTML-Bericht mit Tabelle.
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
    parser.add_argument("--dry-run", action="store_true", help="Nur anzeigen, nichts löschen")
    parser.add_argument("--min-size", type=int, default=0, help="Nur Dateien größer als X KB einbeziehen")
    parser.add_argument("--min-age", type=int, default=0, help="Nur Dateien älter als X Tage einbeziehen")
    args = parser.parse_args()

    print("\n🔍 Starte Bereinigungsscanner...\n")
    logging.info("Cleanup gestartet")

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

        if args.dry_run:
            print("🧪 Dry-Run aktiviert: Es wird nichts gelöscht.")
        elif args.backup:
            print("📦 Starte Backup...")
            zip_result = create_backup(unwanted_files)
            print(f"\n🗂 Backup gespeichert unter: {zip_result}\n")
            logging.info(f"Backup ZIP erstellt: {zip_result}")

        delete_files(unwanted_files, force=args.force, dry_run=args.dry_run)
    else:
        print("✅ Keine verdächtigen Dateien gefunden.")
        logging.info("Keine verdächtigen Dateien gefunden.")

    logging.info("Cleanup abgeschlossen.\n")