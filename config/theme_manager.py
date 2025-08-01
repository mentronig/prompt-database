# config/theme_manager.py

"""
Zentrale Theme-Verwaltung mit Farbspeicherung, SessionState und Farbpaletten.
"""

import streamlit as st
import json
import os

SETTINGS_FILE = "settings/theme.json"


def load_theme():
    """
    Lädt das gespeicherte Theme aus settings/theme.json in den Session-State.
    Fallback ist "Light".
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                st.session_state["theme"] = data.get("theme", "Light")
        except Exception:
            st.session_state["theme"] = "Light"
    else:
        st.session_state["theme"] = "Light"


def save_theme(theme: str):
    """
    Speichert das aktuelle Theme in settings/theme.json.
    """
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"theme": theme}, f)


def get_theme() -> str:
    """
    Gibt das aktuell gesetzte Theme aus dem Session-State zurück.
    """
    return st.session_state.get("theme", "Light")


def is_dark_mode() -> bool:
    """
    True, wenn das aktuelle Theme "Dark" ist.
    """
    return get_theme().lower() == "dark"


def apply_color_scheme(light_color: str, dark_color: str) -> str:
    """
    Gibt die passende Farbe je nach aktuellem Theme zurück.
    """
    return dark_color if is_dark_mode() else light_color


def get_color(role: str) -> str:
    """
    Gibt eine vordefinierte Farbe basierend auf dem Theme und der gewünschten Rolle zurück.

    Rollen: "primary", "secondary", "background", "text"
    """
    palette = {
        "Light": {
            "primary": "#0d6efd",
            "secondary": "#6c757d",
            "background": "#f8f9fa",
            "text": "#212529"
        },
        "Dark": {
            "primary": "#66b2ff",
            "secondary": "#adb5bd",
            "background": "#1e1e1e",
            "text": "#f8f9fa"
        }
    }
    return palette.get(get_theme(), palette["Light"]).get(role, "#000000")


def safe_rerun():
    """
    Führt einen kompatiblen Neustart der App aus – unterstützt alte und neue Streamlit-Versionen.
    """
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()