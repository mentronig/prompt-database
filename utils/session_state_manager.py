# utils/session_state_manager.py

"""
Verwaltet benutzerspezifische Session-Daten in Streamlit.
Speichert z. B. zuletzt bearbeiteten Prompt oder Filterzustände.
"""

import streamlit as st


def set_last_prompt_id(doc_id: str):
    """
    Speichert die zuletzt bearbeitete Prompt-ID.
    :param doc_id: Dokumenten-ID (TinyDB)
    """
    st.session_state["last_prompt_id"] = doc_id


def get_last_prompt_id() -> str | None:
    """
    Gibt die zuletzt bearbeitete Prompt-ID zurück.
    :return: str oder None
    """
    return st.session_state.get("last_prompt_id")


def clear_last_prompt_id():
    """
    Entfernt die gespeicherte Prompt-ID aus dem Session-State.
    """
    if "last_prompt_id" in st.session_state:
        del st.session_state["last_prompt_id"]



