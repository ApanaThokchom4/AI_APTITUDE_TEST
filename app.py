import sys, os

# ── Guarantee the folder containing app.py is FIRST on sys.path ──────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import streamlit as st

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Import pages using importlib (100% path-safe) ─────────────────────
import importlib.util, types

def load_module(name: str, filepath: str):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

P = os.path.join(ROOT, "pages_ui")
C = os.path.join(ROOT, "core")

# Load core modules first so pages can import them
styles          = load_module("core.styles",          os.path.join(C, "styles.py"))
resume_parser   = load_module("core.resume_parser",   os.path.join(C, "resume_parser.py"))
questions       = load_module("core.questions",       os.path.join(C, "questions.py"))
feedback_engine = load_module("core.feedback_engine", os.path.join(C, "feedback_engine.py"))

# Load page modules
landing      = load_module("pages_ui.landing",       os.path.join(P, "landing.py"))
upload       = load_module("pages_ui.upload",        os.path.join(P, "upload.py"))
job_selection= load_module("pages_ui.job_selection", os.path.join(P, "job_selection.py"))
exam         = load_module("pages_ui.exam",          os.path.join(P, "exam.py"))
results      = load_module("pages_ui.results",       os.path.join(P, "results.py"))
feedback     = load_module("pages_ui.feedback",      os.path.join(P, "feedback.py"))

# ── Session-state defaults ────────────────────────────────────────────
DEFAULTS = {
    "page":                "landing",
    "candidate_name":      "",
    "resume_text":         "",
    "detected_skills":     [],
    "job_role":            "",
    "difficulty":          "",
    "subjects_selected":   [],
    "exam_scores":         {},
    "exam_answers":        {},
    "current_subject_idx": 0,
    "exam_started":        False,
    "exam_complete":       False,
    "feedback_data":       None,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Router ────────────────────────────────────────────────────────────
PAGE_MAP = {
    "landing":       landing.show,
    "upload":        upload.show,
    "job_selection": job_selection.show,
    "exam":          exam.show,
    "results":       results.show,
    "feedback":      feedback.show,
}

page_fn = PAGE_MAP.get(st.session_state.page, landing.show)
page_fn()
