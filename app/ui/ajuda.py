import streamlit as st
from pathlib import Path
from app.ui.theme import apply_theme


def ajuda_page():
    apply_theme()
    st.title("Ajuda")
    manual_path = Path("Manual.md")
    if manual_path.exists():
        text = manual_path.read_text(encoding="utf-8")
        st.markdown(text)
    else:
        st.warning("Manual.md não encontrado.")


if __name__ == "__main__":
    ajuda_page()
