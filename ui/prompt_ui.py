"""
PromptDatabaseUI – Streamlit-basierte Benutzeroberfläche zur Verwaltung von AI-Prompts.
"""

import streamlit as st
from services.prompt_service import PromptService
from utils.helpers import export_prompts_to_csv, export_prompts_to_markdown
from utils.backup import backup_database
from utils.project_zipper import zip_project
from utils.logger import configure_logger
from config.theme_manager import get_theme, apply_color_scheme
import subprocess
from streamlit_option_menu import option_menu

logger = configure_logger(__name__)


class PromptDatabaseUI:
    """
    Streamlit-Oberfläche für das Erfassen, Durchsuchen und Bearbeiten von Prompts.
    """

    def __init__(self):
        self.service = PromptService()
        self.edit_mode = False
        self.edit_doc_id = None

    def run(self):
        """Startet die UI mit Icon-Menü."""
        st.set_page_config(page_title="Prompt-Datenbank", layout="wide")
        st.title("🧠 Prompt-Datenbank")

        selected = option_menu(
            menu_title=None,
            options=["Prompts", "Tests", "Backup", "Einstellungen", "Über"],
            icons=["file-earmark-text", "bug", "cloud-download", "gear", "info-circle"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "nav-link": {"font-size": "16px", "padding": "10px 15px"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            }
        )

        if selected == "Prompts":
            st.caption("📋 Erstellen, durchsuchen und verwalten Sie Ihre Prompts.")
            self._show_input_form()
            st.markdown("---")
            self._show_prompt_table()

        elif selected == "Tests":
            st.caption("🧪 Führen Sie Unittests für Ihre Anwendung aus.")
            st.subheader("🧪 Tests ausführen (run_tests.py)")
            button_style = apply_color_scheme("light", "secondary")
            if st.button("Jetzt testen", type=button_style):
                result = subprocess.run(["python", "run_tests.py"], capture_output=True, text=True)
                st.code(result.stdout + result.stderr, language="bash")

        elif selected == "Backup":
            self._show_backup()

        elif selected == "Einstellungen":
            self._show_settings()

        elif selected == "Über":
            self._show_about()

    def _show_backup(self):
        st.subheader("💾 Backup & Projektarchiv")
        button_style = apply_color_scheme("primary", "secondary")
        if st.button("Backup der Datenbank erstellen", type=button_style):
            path = backup_database()
            st.success(f"Backup gespeichert: {path}")

        if st.button("📦 Projektstruktur als ZIP sichern", type=button_style):
            zip_project()
            st.success("Projektstruktur als ZIP gespeichert.")

    def _show_settings(self):
        st.subheader("⚙️ Einstellungen")
        theme = st.radio("Theme wählen", ["Light", "Dark"], index=0)
        st.session_state["theme"] = theme
        st.info(f"Aktuelles Theme: {theme}")

    def _show_about(self):
        st.subheader("ℹ️ Über diese App")
        st.markdown("""
        **Prompt-Datenbank** zum strukturierten Erfassen, Verwalten und Exportieren von KI-Prompts.  
        Entwickelt mit [Streamlit](https://streamlit.io), [TinyDB](https://tinydb.readthedocs.io/)  
        & ❤️ für produktive AI-Nutzung.

        Version: 1.0.0  
        Autor: Dein Projektname / Teamname  
        Lizenz: MIT
        """)

    def _show_input_form(self):
        st.subheader("➕ Prompt hinzufügen" if not self.edit_mode else "✏️ Prompt bearbeiten")

        with st.form(key="prompt_form", clear_on_submit=not self.edit_mode):
            title = st.text_input("Titel", value="")
            category = st.text_input("Kategorie", value="")
            platform = st.selectbox("Plattform", ["ChatGPT", "Claude", "Gemini", "Andere"])
            language = st.text_input("Sprache (optional)", value="")
            purpose = st.text_input("Zweck / Verwendungsziel", value="")
            tags_input = st.text_input("Tags (durch Komma getrennt)", value="")
            prompt_text = st.text_area("Prompt-Text", height=150)
            notes = st.text_area("Notizen (optional)", height=100)

            submit = st.form_submit_button("Prompt speichern")

            if submit:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                try:
                    if self.edit_mode:
                        self.service.update_prompt(self.edit_doc_id, {
                            "title": title,
                            "category": category,
                            "platform": platform,
                            "tags": tags,
                            "prompt": prompt_text,
                            "language": language,
                            "purpose": purpose,
                            "notes": notes
                        })
                        st.success("Prompt erfolgreich aktualisiert.")
                        logger.info("Prompt aktualisiert: ID %s", self.edit_doc_id)
                        self.edit_mode = False
                        self.edit_doc_id = None
                    else:
                        doc_id = self.service.create_prompt(
                            title, category, platform, tags, prompt_text, language, purpose, notes
                        )
                        st.success(f"Prompt gespeichert (ID: {doc_id})")
                        logger.info("Neuer Prompt gespeichert: ID %s", doc_id)
                except ValueError as ve:
                    st.error(str(ve))
                    logger.warning("Validierungsfehler: %s", str(ve))

    def _show_prompt_table(self):
        st.subheader("🔍 Prompts durchsuchen")

        theme = get_theme()
        keyword = st.text_input("Suchbegriff (Titel oder Prompt-Inhalt)")
        category_filter = st.selectbox("Kategorie-Filter", ["Alle"] + self.service.get_all_categories())
        tag_filter = st.multiselect("Tags auswählen", self.service.get_all_tags())
        language_filter = st.text_input("Sprache (optional)")
        purpose_filter = st.text_input("Zweck / Verwendungsziel (optional)")

        filtered_prompts = self.service.search_prompts(
            keyword=keyword,
            category=None if category_filter == "Alle" else category_filter,
            tags=tag_filter
        )

        if language_filter:
            filtered_prompts = [r for r in filtered_prompts if language_filter.lower() in r.get("language", "").lower()]
        if purpose_filter:
            filtered_prompts = [r for r in filtered_prompts if purpose_filter.lower() in r.get("purpose", "").lower()]

        st.write(f"🔎 {len(filtered_prompts)} Prompts gefunden")

        with st.expander("📤 Export & Sicherung", expanded=False):
            export_choice = st.selectbox("Aktion wählen:", [
                "-- bitte wählen --",
                "Export als CSV",
                "Export als Markdown",
                "Datenbank Backup",
                "Projektstruktur ZIP"
            ])
            button_style = apply_color_scheme("primary", "secondary")
            if st.button("Ausführen", type=button_style):
                if export_choice == "Export als CSV":
                    export_prompts_to_csv(filtered_prompts)
                    st.success("CSV exportiert.")
                elif export_choice == "Export als Markdown":
                    export_prompts_to_markdown(filtered_prompts)
                    st.success("Markdown exportiert.")
                elif export_choice == "Datenbank Backup":
                    path = backup_database()
                    st.success(f"Backup gespeichert: {path}")
                elif export_choice == "Projektstruktur ZIP":
                    zip_project()
                    st.success("Projektstruktur gespeichert.")

        for prompt in filtered_prompts:
            with st.expander(f"{prompt['title']} ({prompt['category']})", expanded=False):
                st.markdown(f"**Plattform:** {prompt['platform']}")
                st.markdown(f"**Sprache:** {prompt.get('language', '-')}")
                st.markdown(f"**Zweck:** {prompt.get('purpose', '-')}")
                st.markdown(f"**Tags:** {', '.join(prompt['tags'])}")
                st.markdown(f"**Letzte Änderung:** {prompt['last_modified']}")
                st.markdown(f"**Prompt:**\n\n```text\n{prompt['prompt']}\n```")
                st.markdown(f"**Notizen:**\n{prompt.get('notes', '-')}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Bearbeiten", key=f"edit_{prompt.doc_id}"):
                        self.edit_mode = True
                        self.edit_doc_id = prompt.doc_id
                        logger.info("Bearbeitungsmodus aktiviert: ID %s", prompt.doc_id)
                        st.experimental_rerun()
                with col2:
                    if st.button("🗑️ Löschen", key=f"delete_{prompt.doc_id}"):
                        self.service.delete_prompt(prompt.doc_id)
                        st.success("Prompt gelöscht.")
                        logger.info("Prompt gelöscht: ID %s", prompt.doc_id)
                        st.experimental_rerun()