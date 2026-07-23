import streamlit as st

PRIMARY_BLUE = "#2563eb"
LIGHT_BLUE = "#eff6ff"
MID_BLUE = "#dbeafe"
DARK_TEXT = "#0f172a"
MUTED_TEXT = "#64748b"
CARD_BORDER = "#e2e8f0"


def inject_css() -> None:
    """Apply lightweight dashboard styling without external dependencies."""
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: linear-gradient(180deg, #f8fbff 0%, #ffffff 44%);
                color: {DARK_TEXT};
            }}

            [data-testid="stSidebar"] {{
                background: #ffffff;
                border-right: 1px solid {CARD_BORDER};
            }}

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] p {{
                color: {DARK_TEXT};
            }}

            div[data-testid="stMetric"] {{
                background: #ffffff;
                border: 1px solid {CARD_BORDER};
                border-radius: 18px;
                padding: 18px 18px 14px;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
                min-height: 124px;
            }}

            div[data-testid="stMetric"] label {{
                color: {MUTED_TEXT};
                font-weight: 700;
            }}

            div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
                color: {DARK_TEXT};
                font-weight: 800;
            }}

            .section-title {{
                margin: 0 0 0.35rem;
                color: {DARK_TEXT};
                font-size: 1.25rem;
                font-weight: 800;
            }}

            .section-subtitle {{
                margin: 0 0 1rem;
                color: {MUTED_TEXT};
                font-size: 0.95rem;
            }}

            .app-hero {{
                background: linear-gradient(135deg, #ffffff 0%, {LIGHT_BLUE} 100%);
                border: 1px solid {MID_BLUE};
                border-radius: 22px;
                padding: 26px 28px;
                margin-bottom: 22px;
                box-shadow: 0 18px 40px rgba(37, 99, 235, 0.08);
            }}

            .app-hero h1 {{
                margin: 0;
                color: {DARK_TEXT};
                font-size: clamp(2rem, 4vw, 3.15rem);
                font-weight: 850;
                letter-spacing: 0;
            }}

            .app-hero p {{
                margin: 0.55rem 0 0;
                max-width: 780px;
                color: {MUTED_TEXT};
                font-size: 1.05rem;
                line-height: 1.55;
            }}

            .card {{
                background: #ffffff;
                border: 1px solid {CARD_BORDER};
                border-radius: 18px;
                padding: 18px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
                height: 100%;
            }}

            .mini-card {{
                background: {LIGHT_BLUE};
                border: 1px solid {MID_BLUE};
                border-radius: 16px;
                padding: 14px 16px;
                height: 100%;
            }}

            .pill {{
                display: inline-block;
                padding: 0.28rem 0.6rem;
                margin: 0.12rem;
                border-radius: 999px;
                background: {LIGHT_BLUE};
                color: #1d4ed8;
                border: 1px solid {MID_BLUE};
                font-size: 0.8rem;
                font-weight: 700;
            }}

            .fit-pro-item {{
                background: #f0fdf4;
                border-left: 4px solid #15803d;
                padding: 8px 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                color: #166534;
                font-size: 0.9rem;
                font-weight: 500;
                line-height: 1.4;
            }}

            .fit-con-item {{
                background: #fef2f2;
                border-left: 4px solid #b91c1c;
                padding: 8px 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                color: #991b1b;
                font-size: 0.9rem;
                font-weight: 500;
                line-height: 1.4;
            }}

            .email-container {{
                background: #ffffff;
                border: 1px solid {CARD_BORDER};
                border-radius: 12px;
                padding: 20px;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
                font-family: 'Inter', sans-serif;
                white-space: pre-wrap;
                font-size: 0.95rem;
                line-height: 1.6;
                color: {DARK_TEXT};
                min-height: 300px;
            }}

            .email-subject {{
                font-weight: 700;
                border-bottom: 1px solid {CARD_BORDER};
                padding-bottom: 10px;
                margin-bottom: 15px;
                font-size: 1rem;
                color: {DARK_TEXT};
            }}

            .status-open, .status-active, .status-selected {{
                color: #047857;
                background: #ecfdf5;
                border-color: #a7f3d0;
            }}

            .status-review, .status-scheduled {{
                color: #1d4ed8;
                background: {LIGHT_BLUE};
                border-color: {MID_BLUE};
            }}

            .status-hold, .status-draft {{
                color: #92400e;
                background: #fffbeb;
                border-color: #fde68a;
            }}

            .progress-track {{
                width: 100%;
                height: 10px;
                background: #e5e7eb;
                border-radius: 999px;
                overflow: hidden;
            }}

            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #38bdf8, {PRIMARY_BLUE});
                border-radius: 999px;
            }}

            .stButton > button {{
                border-radius: 12px;
                border: 1px solid {MID_BLUE};
                background: #ffffff;
                color: {PRIMARY_BLUE};
                font-weight: 750;
            }}

            .stButton > button:hover {{
                border-color: {PRIMARY_BLUE};
                color: #1d4ed8;
                background: {LIGHT_BLUE};
            }}

            .stDataFrame {{
                border: 1px solid {CARD_BORDER};
                border-radius: 16px;
                overflow: hidden;
            }}

            .question-card {{
                background: #ffffff;
                border: 1px solid {CARD_BORDER};
                border-left: 4px solid {PRIMARY_BLUE};
                border-radius: 14px;
                padding: 16px 20px;
                margin-bottom: 14px;
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
                word-wrap: break-word;
                overflow-wrap: anywhere;
                word-break: break-word;
                white-space: normal;
                max-width: 100%;
                box-sizing: border-box;
            }}

            .question-title {{
                font-weight: 750;
                font-size: 1.02rem;
                color: {DARK_TEXT};
                margin-bottom: 6px;
                line-height: 1.5;
                word-wrap: break-word;
                overflow-wrap: anywhere;
                word-break: break-word;
                white-space: normal;
            }}

            .question-note {{
                font-size: 0.88rem;
                color: {MUTED_TEXT};
                background: {LIGHT_BLUE};
                border: 1px solid {MID_BLUE};
                padding: 10px 14px;
                border-radius: 10px;
                margin-top: 8px;
                line-height: 1.5;
                word-wrap: break-word;
                overflow-wrap: anywhere;
                word-break: break-word;
                white-space: normal;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
