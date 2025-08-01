# 🧹 PromptDatabase – Cleanup Tool (v0.8)

Ein praktisches CLI-Tool zur Bereinigung von überflüssigen Python-Dateien – ideal zur Projektpflege in Visual Studio, VS Code und Co.

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

