# 🧹 PromptDatabase – Cleanup Tool

Dieses Projekt enthält ein optionales CLI-Werkzeug zur automatischen Bereinigung von überflüssigen Python-Dateien – insbesondere temporäre oder versehentlich erstellte Skripte wie `klasse1.py`, `test.py`, `experiment_alt.py` etc.

---

## ⚙️ Features des Cleanup-Skripts

| Funktion                | Beschreibung                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| 🔍 Dateinamens-Scanner  | Erkennt `.py`-Dateien mit unerwünschten Namen (z. B. `test`, `klasse`, etc.) |
| 📏 Filter               | Optional nach Größe (`--min-size`) und Alter (`--min-age`) filterbar         |
| 💾 Backup               | ZIP-Backup aller zu löschenden Dateien vor dem Entfernen (`--backup`)        |
| ❓ Interaktiv oder Automatisch | Interaktives Löschen oder direkt mit `--force`                          |
| 📝 Berichte             | Generiert HTML- und Markdown-Reports über gefundene Dateien                  |

---

## 📁 Speicherort des Skripts

Das Skript befindet sich im Verzeichnis:
tools/