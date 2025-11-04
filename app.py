
import streamlit as st
from agents import AgentManager
from utils.logger import logger
import os
from dotenv import load_dotenv
from agents import PDFTextAgent

load_dotenv()



def get_design_tokens(mode: str):
    light = {
        "mode": "light",
        "primary": "#2563EB",
        "primary_rgb": "37,99,235",
        "accent": "#F59E0B",
        "bg": "#F5F7FA",
        "panel": "#FFFFFF",
        "panel_alt": "#F0F3F8",
        "border": "#E2E8F0",
        "text": "#1F2430",
        "muted": "#5F6B7A",
        "success": "#15803D",
        "warning": "#B45309",
        "danger": "#B91C1C",
        "code_bg": "#1E293B",
    }
    dark = {
        "mode": "dark",
        "primary": "#3B82F6",
        "primary_rgb": "59,130,246",
        "accent": "#FBBF24",
        "bg": "#121417",
        "panel": "#1B1F24",
        "panel_alt": "#242A31",
        "border": "#2C333C",
        "text": "#E9EDF2",
        "muted": "#8B97A5",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "code_bg": "#0F172A",
    }
    return dark if mode == "Dark" else light

def inject_theme_css(tokens: dict):
    st.markdown(f"""
    <style>
    :root {{
        --color-bg: {tokens['bg']};
        --color-panel: {tokens['panel']};
        --color-panel-alt: {tokens['panel_alt']};
        --color-border: {tokens['border']};
        --color-text: {tokens['text']};
        --color-muted: {tokens['muted']};
        --color-primary: {tokens['primary']};
        --color-primary-rgb: {tokens['primary_rgb']};
        --color-accent: {tokens['accent']};
        --color-success: {tokens['success']};
        --color-warning: {tokens['warning']};
        --color-danger: {tokens['danger']};
        --color-code-bg: {tokens['code_bg']};
        --radius-sm: 6px;
        --radius: 14px;
        --radius-lg: 22px;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.06);
        --shadow: 0 4px 14px -4px rgba(0,0,0,0.15);
        --shadow-hover: 0 8px 26px -6px rgba(0,0,0,0.25);
        --font-stack: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    html, body, .stApp {{
        background: var(--color-bg);
        color: var(--color-text);
        font-family: var(--font-stack);
    }}
    .block-container {{padding-top:1.4rem; padding-bottom:4rem; max-width: 1420px;}}
    h1,h2,h3,h4,h5 {{
        font-weight:600;
        letter-spacing:.4px;
    }}
    h1 {{
        font-size: clamp(2.35rem, 4vw, 3rem);
        line-height:1.1;
        background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
        -webkit-background-clip:text;
        color: transparent;
        font-weight:700;
        margin-bottom:.35rem;
    }}
    h2 {{font-size:1.55rem; margin-top:1.8rem;}}
    p, li {{font-size:0.95rem; line-height:1.5rem;}}
    small, .small-note {{font-size:0.72rem; color:var(--color-muted);}}

    /* Hero Section */
    .hero-wrapper {{
        position: relative;
        overflow:hidden;
        border-radius: var(--radius-lg);
        padding: 2.6rem clamp(1.6rem, 3vw, 3rem);
        background:
          linear-gradient(135deg, rgba(var(--color-primary-rgb),0.15), rgba(255,255,255,0) 70%),
          linear-gradient(195deg, var(--color-panel) 0%, var(--color-panel-alt) 100%);
        border:1px solid var(--color-border);
        box-shadow: var(--shadow);
    }}
    .hero-wrapper:before {{
        content:"";
        position:absolute;
        top:-25%; left:-10%;
        width:60%; height:160%;
        background:radial-gradient(circle at center, rgba(var(--color-primary-rgb),0.25), transparent 70%);
        opacity:.35;
        pointer-events:none;
        filter:blur(42px);
    }}

    /* Feature Pills */
    .feature-pill {{
        display:inline-flex;
        align-items:center;
        gap:.4rem;
        padding:.45rem .85rem;
        background: var(--color-panel-alt);
        border:1px solid var(--color-border);
        color: var(--color-muted);
        font-size:.7rem;
        font-weight:600;
        letter-spacing:.08em;
        text-transform:uppercase;
        border-radius: 40px;
        margin: .25rem .4rem .25rem 0;
        transition:.18s;
    }}
    .feature-pill:hover {{color: var(--color-text); border-color: var(--color-primary);}}

    /* +++ ADDED: feature-badge style (was missing) +++ */
    .feature-badge {{
        display:inline-block;
        padding:.35rem .70rem;
        background: var(--color-panel-alt);
        border:1px solid var(--color-border);
        color: var(--color-muted);
        font-size:.65rem;
        font-weight:600;
        letter-spacing:.05em;
        text-transform:uppercase;
        border-radius: 999px;
        margin:.2rem .35rem .2rem 0;
        transition:.18s;
    }}
    .feature-badge:hover {{
        color: var(--color-text);
        border-color: var(--color-primary);
        background: var(--color-panel);
    }}
    /* --- END added --- */

    /* Cards (Steps / Panels) */
    .mini-card {{
        background: var(--color-panel);
        border:1px solid var(--color-border);
        border-radius: var(--radius);
        padding: .95rem 1rem;
        position:relative;
        box-shadow: var(--shadow-sm);
        transition:.18s;
        min-height: 120px;
    }}
    .mini-card:hover {{
        box-shadow: var(--shadow);
        transform: translateY(-3px);
        border-color: var(--color-primary);
    }}
    .mini-icon {{
        font-size:1.3rem;
        line-height:1;
        margin-bottom:.35rem;
        opacity:.85;
    }}
    .mini-card h5 {{
        margin:0 0 .25rem;
        font-size:.85rem;
        letter-spacing:.05em;
        text-transform:uppercase;
        font-weight:600;
        color: var(--color-primary);
    }}
    .mini-card p {{
        font-size:.78rem;
        line-height:1.15rem;
        margin:0;
    }}

    /* Navigation Pills */
    .nav-bar {{
        display:flex;
        gap:.55rem;
        flex-wrap:wrap;
        margin-bottom:1.2rem;
    }}
    .nav-pill {{
        cursor:pointer;
        user-select:none;
        font-size:.8rem;
        font-weight:500;
        background: var(--color-panel);
        border:1px solid var(--color-border);
        color: var(--color-muted);
        padding:.55rem .95rem;
        border-radius: 999px;
        display:inline-flex;
        align-items:center;
        gap:.45rem;
        transition:.22s;
        box-shadow: var(--shadow-sm);
        text-decoration:none;
    }}
    .nav-pill.active {{
        background: linear-gradient(90deg,var(--color-primary), var(--color-accent));
        color:#fff;
        border-color: var(--color-primary);
        box-shadow: var(--shadow);
        font-weight:600;
    }}
    .nav-pill:hover {{
        border-color: var(--color-primary);
        color: var(--color-text);
        transform: translateY(-2px);
    }}

    /* Buttons (override) */
    .stButton>button {{
        border-radius: 12px;
        font-weight:600;
        letter-spacing:.3px;
        padding:.7rem 1.15rem;
        background: var(--color-primary);
        border:1px solid var(--color-primary);
        color:#fff;
        transition:.18s;
        box-shadow: var(--shadow-sm);
    }}
    .stButton>button:hover {{
        filter:brightness(1.08);
        box-shadow: var(--shadow);
        transform: translateY(-2px);
    }}
    .stButton>button:active {{
        transform: translateY(0);
        filter:brightness(.93);
    }}

    /* File Uploader Card */
    [data-testid="stFileUploader"] > div {{
        background: var(--color-panel);
        border:1px dashed var(--color-border);
        padding:1.2rem 1rem;
        border-radius: var(--radius);
        transition:.2s;
    }}
    [data-testid="stFileUploader"] > div:hover {{
        border-color: var(--color-primary);
        background: var(--color-panel-alt);
    }}

    /* Text Areas */
    .stTextArea textarea {{
        font-family: var(--mono);
        font-size: .82rem;
        line-height: 1.3rem;
        border-radius: 10px !important;
    }}

    /* Output boxes */
    .output-box {{
        background: var(--color-panel);
        border:1px solid var(--color-border);
        border-radius: var(--radius);
        padding: .85rem 1rem;
        font-size: .8rem;
        max-height: 280px;
        overflow:auto;
        box-shadow: var(--shadow-sm);
    }}

    /* Expanders */
    details[open] {{
        background: var(--color-panel-alt);
        border-radius: var(--radius-sm);
    }}
    summary {{
        font-weight:600;
    }}

    /* Scrollbar refinement */
    ::-webkit-scrollbar {{
        width:10px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(120,130,150,0.35);
        border-radius: 40px;
        border:2px solid var(--color-bg);
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(120,130,150,0.55);
    }}
    </style>
    """, unsafe_allow_html=True)


def render_nav():
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Home"
        
    pages = [
        ("Home", "🏠"),
        ("CV Recommender", "📄"),
        ("Grammar Tool", "📝"),
        ("Text Anonymizer", "🛡️"),
    ]
    st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
    cols = st.columns(len(pages))
    for i, (label, icon) in enumerate(pages):
        active = (st.session_state.active_page == label)
        if cols[i].button(f"{icon}  {label}", key=f"nav_{label}"):   
            st.session_state.active_page = label

    st.markdown("</div>", unsafe_allow_html=True)
    return st.session_state.active_page


def main():
    st.set_page_config(page_title="Multi-Agent AI System", layout="wide")

    with st.sidebar:
        mode = st.radio("Theme", ["Light", "Dark"], horizontal=False)
        st.markdown("---")
        st.caption("Navigation")
    tokens = get_design_tokens(mode)
    inject_theme_css(tokens)

    st.markdown("<div class='hero-wrapper'>", unsafe_allow_html=True)
    st.markdown("<h1>Multi‑Agent CV and SOP Refinement</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:1.02rem; max-width:860px; color:var(--color-muted);'>A minimalist workspace for elevating CVs and academic documents using a collaborative pipeline: grammar normalization, anonymization, and structured recommendations.</p>",
        unsafe_allow_html=True
    )
   
    st.markdown(
        "".join(
            f"<span class='feature-pill'>{icon} {lbl}</span>"
            for icon, lbl in [
                ("📄", "PDF Parsing"),
                ("🧠", "Contextual Feedback"),
                ("🛡️", "Anonymization"),
                ("⚙️", "Pipeline"),
                ("🔍", "Clarity"),
                ("✅", "Polish")
            ]
        ),
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    agent_manager = AgentManager(max_retries=2, verbose=True)

    active = render_nav()


    if active == "Home":
        render_home()  
    elif active == "CV Recommender":
        cv_recommender_section(agent_manager)
    elif active == "Grammar Tool":
        grammar_checking_section(agent_manager)
    elif active == "Text Anonymizer":
        text_anonymizer_section(agent_manager)


def render_home():
    with st.container():
        st.markdown("<div class='hero-box'>", unsafe_allow_html=True)
        st.subheader("Document Intelligence Workspace")
        st.write(
            "Leverage specialized collaborating agents to optimize academic and professional documents. "
            "Handle grammar normalization, anonymization, and targeted structural recommendations."
        )
        st.markdown(
            " | ".join(
                f"<span class='feature-badge'>{badge}</span>"
                for badge in [
                    "PDF Parsing",
                    "Grammar Normalization",
                    "Anonymization",
                    "Structured CV Feedback",
                    "Multi‑Agent Orchestration"
                ]
            ),
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### How It Works")
    col1, col2, col3 = st.columns(3)
    col1.markdown("<div class='step'><b>1. Input</b><br/>Upload PDF or paste text.</div>", unsafe_allow_html=True)
    col2.markdown("<div class='step'><b>2. Normalize</b><br/>Grammar + anonymization pipeline.</div>", unsafe_allow_html=True)
    col3.markdown("<div class='step'><b>3. Recommend</b><br/>Receive structured improvements.</div>", unsafe_allow_html=True)

    with st.expander("Tips"):
        st.markdown(
            """
            - Upload high-quality, text-based PDFs (not scans) for best extraction.
            """
        )


def grammar_checking_section(agent_manager):
    st.header("Grammar Tool")
    st.caption("Standalone grammar normalization (no anonymization or recommendations).")
    text = st.text_area("Paste text to normalize:", height=260, key="grammar_text")
    col_a, col_b, col_c = st.columns([1,1,1])
    if col_a.button("Normalize Grammar"):
        if not text.strip():
            st.warning("Please enter some text.")
            return
        agent = agent_manager.get_agent("grammar_checker")
        with st.spinner("Normalizing..."):
            try:
                normalized = _ensure_str(agent.execute(text))
                st.markdown("##### Result")
                st.code(normalized, language="markdown")
            except Exception as e:
                st.error("Error during grammar normalization.")
                logger.error(e)
    if col_b.button("Generate Grammar Report"):
        if not text.strip():
            st.warning("Please enter some text.")
            return
        agent = agent_manager.get_agent("grammar_checker")
        with st.spinner("Generating report..."):
            try:
                report = _ensure_str(agent.generate_report(text))
                st.markdown("##### Improvement Report")
                st.markdown(report)
            except Exception as e:
                st.error("Report generation failed.")
                logger.error(e)
    if col_c.button("Clear"):
        st.session_state["grammar_text"] = ""


def cv_recommender_section(agent_manager):
    st.header("CV Recommender")
    st.caption("Pipeline: Grammar → Anonymization → Structured Recommendations.")

    left, right = st.columns([1.05, 1])
    with left:
        st.markdown("<div class='section-label'>Source Input</div>", unsafe_allow_html=True)
        uploaded_pdf = st.file_uploader("Upload CV PDF", type=["pdf"], help="Text-based PDFs only (no scans).")
        extracted_text = ""
        if uploaded_pdf:
            temp_path = "temp_cv.pdf"
            with open(temp_path, "wb") as f:
                f.write(uploaded_pdf.read())
            with st.spinner("Extracting PDF text..."):
                try:
                    pdf_agent = PDFTextAgent()
                    extracted_text = pdf_agent.extract_text(temp_path)  
                except Exception as e:
                    st.error("Failed to extract PDF text.")
                    logger.error(e)

        cv_input_key = "cv_raw_text"
        if cv_input_key not in st.session_state:
            st.session_state[cv_input_key] = extracted_text
        if extracted_text and not st.session_state[cv_input_key].strip():
            st.session_state[cv_input_key] = extracted_text

        new_text = st.text_area(
            "Paste or refine your CV text:",
            value=st.session_state[cv_input_key],
            height=420
        )
        st.session_state[cv_input_key] = new_text

        c1, c2, c3 = st.columns(3)
        run_clicked = c1.button("Run Full Pipeline")
        c2.button("Reset Input", on_click=lambda: st.session_state.update({cv_input_key:""}))
        c3.button("Load Extracted (If Any)", disabled=not extracted_text,
                  on_click=lambda: st.session_state.update({cv_input_key: extracted_text}))

    with right:
        st.markdown("<div class='section-label'>Pipeline Output</div>", unsafe_allow_html=True)
        if run_clicked:
            raw_text = st.session_state[cv_input_key]
            if not raw_text.strip():
                st.warning("Provide CV text before running pipeline.")
                return

            grammar_agent = agent_manager.get_agent("grammar_checker")
            anonymizer_agent = agent_manager.get_agent("text_anonymizer")
            recommender_agent = agent_manager.get_agent("cv_recommender")

            grammar_corrected = None
            anonymized = None
            recommendations = None

            #grammar
            with st.spinner("Step 1/3: Grammar normalization"):
                try:
                    grammar_corrected = _ensure_str(grammar_agent.execute(raw_text))
                    st.markdown("**Grammar‑Normalized Text**")
                    st.text_area("Normalized", grammar_corrected, height=160)
                except Exception as e:
                    st.error("Grammar normalization failed.")
                    logger.error(e)
                    return

            #anonymization
            with st.spinner("Step 2/3: Anonymizing"):
                try:
                    anonymized = _ensure_str(anonymizer_agent.execute(grammar_corrected))
                    st.markdown("**Anonymized Text**")
                    st.text_area("Anonymized", anonymized, height=160)
                except Exception as e:
                    st.error("Anonymization failed.")
                    logger.error(e)
                    return

            #recommendations
            with st.spinner("Step 3/3: Generating recommendations"):
                try:
                    recommendations = recommender_agent.execute(anonymized)
                except Exception as e:
                    st.error("Recommendation generation failed.")
                    logger.error(e)
                    return

            st.markdown("**Structured Recommendations**")
            rec_text = _ensure_str(recommendations)
            parsed_sections = []
            try:
                parsed_sections = parse_cv_recommendations(rec_text)
            except Exception as e:
                logger.warning(f"Parsing recommendations failed: {e}")

            if parsed_sections:
                for sec in parsed_sections:
                    exp_label = f"{'❌ Missing - ' if sec['missing'] else ''}{sec['title']}"
                    with st.expander(exp_label, expanded=sec['missing']):
                        st.markdown("**Original:**")
                        st.write(sec['original'] if sec['original'].strip() else "Not present")
                        st.markdown("**Recommended:**")
                        st.write(sec['recommended'] if sec['recommended'].strip() else "✅ No change needed")
            else:
               
                st.markdown(rec_text)

            
            dl_col1, dl_col2, dl_col3 = st.columns(3)
            if anonymized:
                dl_col1.download_button(
                    "Download Anonymized",
                    anonymized,
                    file_name="cv_anonymized.txt",
                    type="primary"
                )
            if grammar_corrected:
                dl_col2.download_button(
                    "Download Normalized",
                    grammar_corrected,
                    file_name="cv_normalized.txt"
                )
            if rec_text:
                dl_col3.download_button(
                    "Download Recommendations",
                    rec_text,
                    file_name="cv_recommendations.txt"
                )
        else:
            st.info("Run the pipeline to view outputs here.")


def text_anonymizer_section(agent_manager):
    st.header("Text Anonymizer")
    st.caption("Applies anonymization after grammar normalization.")
    original = st.text_area("Enter text:", height=260, key="anon_text")
    col1, col2 = st.columns([1,1])
    if col1.button("Anonymize"):
        if not original.strip():
            st.warning("Input required.")
            return
        grammar_agent = agent_manager.get_agent("grammar_checker")
        anonymizer = agent_manager.get_agent("text_anonymizer")
        with st.spinner("Normalizing..."):
            try:
                norm = _ensure_str(grammar_agent.execute(original))
            except Exception as e:
                st.error("Grammar step failed.")
                logger.error(e)
                return
        with st.spinner("Anonymizing..."):
            try:
                anon = _ensure_str(anonymizer.execute(norm))
            except Exception as e:
                st.error("Anonymization failed.")
                logger.error(e)
                return
        st.markdown("##### Normalized")
        st.code(norm, language="markdown")
        st.markdown("##### Anonymized")
        st.code(anon, language="markdown")
        st.download_button("Download Anonymized", anon, file_name="anonymized.txt")
    if col2.button("Clear"):
        st.session_state["anon_text"] = ""


def _ensure_str(maybe):
    if isinstance(maybe, str):
        return maybe
    if hasattr(maybe, "content"):
        return str(maybe.content)
    return str(maybe)


import re
def parse_cv_recommendations(rec_text: str):
    """
    Parse the formatted CV recommendation output into structured sections.
    Expected block pattern separated by lines containing only ---.
    Returns list[dict]: {title, missing(bool), original, recommended, raw}
    """
    sections = []
    blocks = re.split(r'\n-{3,}\n', rec_text.strip())
    for block in blocks:
        blk = block.strip()
        if not blk:
            continue
        title_match = re.search(r'^\*\*(.+?)\*\*', blk)
        if not title_match:
            continue
        title_line = title_match.group(1).strip()
        missing = "(Missing)" in title_line
        clean_title = title_line.replace("(Missing)", "").strip()
        orig_match = re.search(r'\*\*Original:\*\*\s*\n(.*?)(\n\*\*Recommended:\*\*|\Z)', blk, re.S)
        rec_match  = re.search(r'\*\*Recommended:\*\*\s*\n(.*)', blk, re.S)
        original = (orig_match.group(1).strip() if orig_match else "Not present")
        recommended = (rec_match.group(1).strip() if rec_match else "")
        sections.append({
            "title": clean_title,
            "missing": missing or original.lower() in ["not present", "not present."],
            "original": original,
            "recommended": recommended,
            "raw": blk
        })
    return sections


if __name__ == "__main__":
    main()
    
