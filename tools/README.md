# 🧹 PromptDatabase – Cleanup Tool (v0.8)

Ein praktisches CLI-Tool zur Bereinigung von überflüssigen Python-Dateien – ideal zur Projektpflege in Visual Studio, VS Code und Co.

---
Aktuelle Version: **v0.73**  
Tag im Repository: `v0.73`  
Letztes Update: 2025-08-01

---

## ⚙️ Beispielaufrufe

```bash
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


---

## 🔐 Neue Schutzlogik (ab v0.9)

Produktionsrelevante Dateien wie `utils/backup.py` oder `tests/test_prompt_repository.py`
werden automatisch erkannt und **niemals gelöscht** – auch nicht bei `--force`.

Geschützt werden z. B.:

```python
PROTECTED_PATHS = [
    "tests/test_prompt_repository.py",
    "utils/backup.py"
]

---

## ✨ Features in Version 0.8

| Funktion               | Beschreibung                                                                 |
|------------------------|------------------------------------------------------------------------------|
| 🔍 Schlüsselwort-Scan   | Erkennt `.py`-Dateien mit Namen wie `test`, `tmp`, `klasse`, `alt` etc.     |
| 📏 Filter               | Auswahl nach Dateigröße (`--min-size`) und Alter (`--min-age`)              |
| 💾 Backup               | ZIP-Archiv aller Dateien vor dem Löschen (`--backup`)                       |
| 🧪 Dry-Run-Modus        | Vorschau-Modus ohne Änderungen (`--dry-run`)                                 |
| 📝 Logging              | Alle Aktionen werden in `cleanup.log` protokolliert                         |
| 📊 Berichte             | HTML + Markdown-Report über verdächtige Dateien                             |

---

## 📁 Speicherort

Das Skript befindet sich unter:

