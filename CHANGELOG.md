# 📜 Changelog – PromptDatabase Cleanup Tool

Alle relevanten Änderungen nach Versionen.

---

## [v0.73] – 2025-08-01
### 🚀 Neu
- Schutzfunktion: `utils/` und `tests/`-Dateien wie `backup.py` werden nicht mehr gelöscht
- Schutzliste (`PROTECTED_PATHS`) eingebaut
- Logging aller Aktionen in `cleanup.log`
- Verbesserter Löschablauf mit `force`, `dry-run` und interaktiver Bestätigung
- Dry-Run-Modus simuliert vollständigen Durchlauf ohne Änderungen

### 🛠 Fixes
- `--force` ignorierte vorherige Schutzlogik → jetzt robust geschützt
- Sonderzeichenprobleme im CMD-Output entschärft

---

## [v0.71] – 2025-07-31
### 🚀 Neu
- Logging in `cleanup.log` integriert
- Dry-Run-Modus (`--dry-run`) eingeführt
- Fehlerprotokollierung mit Logging-Level `INFO`/`ERROR`
- ZIP-Backup vor dem Löschen (`--backup`)
- HTML- und Markdown-Berichte

---

## [v0.7] – 2025-07-30
### 🧹 Erste Version
- Cleanup-Tool erkennt verdächtige `.py`-Dateien nach Namen
- Optionales Löschen mit Benutzerabfrage
- Berichte in HTML/Markdown
