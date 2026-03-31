import streamlit as st

# Paleta centralizada
PALETTE = {
    "bg": "#0d1726",
    "card": "#101c2c",
    "card_alt": "#122035",
    "stroke": "#1f2e45",
    "accent": "#3fb8af",
    "warning": "#f6a609",
    "danger": "#e04f5f",
    "muted": "#9fb3d1",
    "text": "#e9f1ff",
    "shadow": "0 20px 60px rgba(0,0,0,0.35)",
}


def apply_theme():
    st.set_page_config(page_title="Avaliação Docente", layout="wide")
    st.markdown(
        f"""
        <style>
        :root {{
            --bg: {PALETTE['bg']};
            --card: {PALETTE['card']};
            --stroke: {PALETTE['stroke']};
            --text: {PALETTE['text']};
            --muted: {PALETTE['muted']};
            --accent: {PALETTE['accent']};
            --warn: {PALETTE['warning']};
            --danger: {PALETTE['danger']};
            --shadow: {PALETTE['shadow']};
        }}
        body {{
            background: linear-gradient(180deg, #0b1522 0%, #0a1220 100%);
            color: var(--text);
        }}
        .stApp {{
            background: transparent;
        }}
        div.block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}
        .card {{
            background: var(--card);
            border: 1px solid var(--stroke);
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: var(--shadow);
        }}
        .metric-title {{
            font-weight: 800;
            letter-spacing: 0.2px;
        }}
        .muted {{
            color: var(--muted);
            font-size: 0.9rem;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            border: 1px solid transparent;
        }}
        .badge.low {{ background: rgba(63,184,175,0.15); color: var(--accent); border-color: rgba(63,184,175,0.35); }}
        .badge.mid {{ background: rgba(246,166,9,0.12); color: var(--warn); border-color: rgba(246,166,9,0.3); }}
        .badge.high {{ background: rgba(224,79,95,0.12); color: var(--danger); border-color: rgba(224,79,95,0.3); }}
        .table thead tr th {{ color: var(--muted); }}
        .stButton>button {{
            background: var(--accent);
            color: #0b1522;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(63,184,175,0.25);
        }}
        .stButton>button:hover {{ filter: brightness(1.08); }}
        .empty-state {{
            border: 1px dashed var(--stroke);
            border-radius: 12px;
            padding: 18px;
            color: var(--muted);
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
