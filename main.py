"""
main.py – Einstiegspunkt für die Streamlit-basierte Prompt-Datenbank

🔧 Startanleitung:

1. Installiere alle Abhängigkeiten:
   > pip install -r requirements.txt

2. Starte die Anwendung mit:
   > streamlit run main.py

3. Du kannst die Oberfläche anschließend im Browser unter
   http://localhost:8501 aufrufen.

📁 Struktur:
- UI-Klasse: PromptDatabaseUI (in ui/prompt_ui.py)
- Geschäftslogik: PromptService (in services/prompt_service.py)
- Datenzugriff: PromptRepository (in models/prompt_model.py)
"""
from ui.prompt_ui import PromptDatabaseUI

if __name__ == "__main__":
    app = PromptDatabaseUI()
    app.run()