# 📘 PromptDatabase

**PromptDatabase** ist eine lokale, leichtgewichtige Prompt-Management-Anwendung mit moderner Streamlit-Oberfläche.  
Sie dient zur Speicherung, Organisation, Filterung und zum Export von KI-Prompts – mit Fokus auf Übersicht, Geschwindigkeit und Personalisierung.

---

## 🚀 Features

| Kategorie        | Beschreibung                                                                 |
|------------------|------------------------------------------------------------------------------|
| 🧠 Prompt-Archiv  | Prompts speichern, durchsuchen, bearbeiten, filtern                         |
| 🏷 Tags & Kategorien | Unterstützt freie Tags + Mehrfachkategorien                              |
| 📁 TinyDB         | JSON-basierte lokale Datenbank – keine Installation notwendig               |
| 🌓 Theme-Switch   | Dark-/Light-Mode + anpassbare Farben über `theme_manager.py`                |
| 🔍 Filter & Suche | Suche nach Titel, Kategorie, Tags, Sprache (`language`), Zweck (`purpose`) |
| 💬 Notizen        | Freitextfeld für persönliche Kommentare zu jedem Prompt                     |
| 📦 Export         | Als CSV / Markdown-Datei exportieren (Einzeln oder komplett)               |
| 🧾 ZIP-Funktion   | ZIP-Archiv mit Projektstruktur + Datenbank auf Knopfdruck                   |
| 🔐 Backup         | Datenbank-Backup mit Zeitstempel auf Knopfdruck                             |
| 🧪 Testsuite      | Automatisierte Tests für Repository-Funktionalität                          |
| 🛠 Tools          | Cleanup-Skript mit Schutzlogik zur Projektbereinigung                       |

---

## 📂 Projektstruktur

```bash
PromptDatabase/
├── main.py                     # Startpunkt der App
├── ui/
│   └── prompt_ui.py           # Streamlit-Oberfläche (UI)
├── data/
│   └── prompts.json           # Datenbank (TinyDB)
├── repository/
│   └── prompt_repository.py   # Zugriffsschicht für DB
├── service/
│   └── prompt_service.py      # Geschäftslogik für Prompts
├── utils/
│   ├── backup.py              # Datenbank-Backup
│   ├── project_zipper.py      # ZIP-Erstellung für Projektstruktur
│   └── theme_manager.py       # Theme-Farbverwaltung & Persistenz
├── tests/
│   └── test_prompt_repository.py  # Testfälle für Repository
├── tools/
│   └── cleanup_suggestions.py     # intelligentes Bereinigungs-Skript
├── requirements.txt           # Alle Abhängigkeiten
└── README.md
```

---

## 🧪 Installation

```bash
git clone https://github.com/mentronig/prompt-database.git
cd prompt-database
pip install -r requirements.txt
```

---

## 🚀 Anwendung starten

```bash
python main.py
```

➡ Streamlit öffnet sich automatisch im Browser (`http://localhost:8501`)

---

## ⚙️ Interaktive Features

- 🔄 Theme-Wechsel: im Menü „Einstellungen“ → speichert dauerhaft Light/Dark-Mode
- 🔧 Projektoptionen: Backup, ZIP-Export, Markdown/CSV-Export im Symbolmenü
- 🧭 Navigation: Horizontalmenü mit Icons + Tooltips

---

## 📤 Export & Backup

- Export als CSV / Markdown: mit allen Feldern (inkl. `language`, `purpose`, `notes`)
- Backup: JSON-Datei mit Zeitstempel
- Projekt-Export: ZIP mit Projektstruktur & Datenbank

---

## 🛡 Cleanup-Tool

Siehe `tools/cleanup_suggestions.py`:

- Filter nach Dateigröße und Alter
- ZIP-Backup vor Löschung
- Dry-Run-Modus
- Schutzliste (`PROTECTED_PATHS`)
- Logging in `cleanup.log`

---

## 🧪 Tests ausführen

```bash
python -m unittest discover -s tests
```

oder schöner:

```bash
python run_tests.py
```

---

## 📅 Roadmap (Auszug)

| Version | Ziel/Fokus                              |
|---------|------------------------------------------|
| v1.0    | Multi-User-Unterstützung, Dashboards     |
| v1.1    | Agentenverwaltung (Rollen, Templates)    |
| v1.2    | Text-to-Speech, mobile UI                |
| v2.0    | Cloud-Sync (optional), Nutzerrechte      |

---

## 📃 Lizenz

MIT License (offen für private und kommerzielle Nutzung)
