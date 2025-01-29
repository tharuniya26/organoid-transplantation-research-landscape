"""Build the scientific report from its XeLaTeX source.

The build is isolated under ``.work/latex_report`` so auxiliary files do not
enter the public report directory. XeLaTeX is required because the manuscript
loads the Windows Times New Roman font files directly.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SOURCE = REPORTS / "organoid_transplantation_evidence_mapping.tex"
BUILD = ROOT / ".work" / "latex_report"
OUTPUT = REPORTS / "organoid_transplantation_evidence_mapping.pdf"


def run(command: list[str], *, cwd: Path) -> None:
    """Run one report-build command and surface its complete failure log."""
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode:
        tail = "\n".join(result.stdout.splitlines()[-120:])
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{tail}")


def main() -> None:
    if shutil.which("xelatex") is None or shutil.which("bibtex") is None:
        raise RuntimeError("XeLaTeX and BibTeX must be installed and available on PATH")

    BUILD.mkdir(parents=True, exist_ok=True)
    tex_command = [
        "xelatex",
        "-enable-installer",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={BUILD}",
        SOURCE.name,
    ]
    run(tex_command, cwd=REPORTS)
    # Run BibTeX from the source directory so the manuscript's
    # ``../references/bibliography`` path resolves consistently.
    bibtex_target = Path("..") / BUILD.relative_to(ROOT) / SOURCE.stem
    run(["bibtex", str(bibtex_target)], cwd=REPORTS)
    run(tex_command, cwd=REPORTS)
    run(tex_command, cwd=REPORTS)

    built_pdf = BUILD / SOURCE.with_suffix(".pdf").name
    shutil.copy2(built_pdf, OUTPUT)
    print(f"Rendered {OUTPUT.relative_to(ROOT)} with XeLaTeX, Times New Roman, and numeric Vancouver-style citations")


if __name__ == "__main__":
    main()
