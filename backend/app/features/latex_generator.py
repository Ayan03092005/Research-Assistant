import re
from uuid import uuid4
from pathlib import Path
from ..io.schemas import LatexRequest, LatexResponse

OUT_DIR = Path(__file__).resolve().parents[2] / "exports"
OUT_DIR.mkdir(exist_ok=True)

# 🔧 All LaTeX braces {{ }} except the {content} placeholder
TEMPLATE = r"""
\documentclass{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}
\usepackage{{setspace}}
\usepackage{{titlesec}}
\usepackage{{lipsum}}
\title{{Generated Research Paper}}
\date{{}}
\begin{{document}}
\maketitle
\onehalfspacing

% --- Content ---
{content}

\end{{document}}
"""

# LaTeX special characters that need escaping
LATEX_SPECIALS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in normal text."""
    return re.sub(
        r"[&%$#_{}~^\\]",
        lambda m: LATEX_SPECIALS.get(m.group(0), m.group(0)),
        text,
    )

def generate_latex_package(payload: LatexRequest, db, current):
    """
    Accepts plain text and safely converts it into a valid LaTeX manuscript file.
    """
    safe_text = escape_latex(payload.draft_markdown)
    tex = TEMPLATE.format(content=safe_text)

    name = f"{uuid4().hex}.tex"
    path = OUT_DIR / name
    path.write_text(tex, encoding="utf-8")

    # Return .tex path for now (PDF generation optional)
    return LatexResponse(zip_url=str(path))
