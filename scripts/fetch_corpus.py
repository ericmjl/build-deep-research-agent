# /// script
# dependencies = ["arxiv", "pymupdf", "requests", "beautifulsoup4"]
# ///
"""Fetch the Part 3 corpus: >=30 full-text papers from arXiv + JOSS.

Outputs Markdown files (YAML-ish frontmatter + body) under
``build_deep_research_agent/fixtures/corpus/``. Only extracted text is
committed (no PDFs). Re-run to refresh.

Run: ``uv run scripts/fetch_corpus.py``
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import arxiv
import fitz  # pymupdf
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "build_deep_research_agent"
    / "fixtures"
    / "corpus"
)
UA = "tutorial-fetcher/1.0 (https://github.com/ericmjl/build-deep-research-agent)"

# (arxiv category, query terms, domain tag, count)
ARXIV_PULLS = [
    ("cs.AI", "large language model", "ai", 5),
    ("cs.LG", "representation learning", "ai", 4),
    ("astro-ph.GA", "galaxy formation", "astrophysics", 4),
    ("astro-ph.CO", "dark energy cosmology", "astrophysics", 4),
    ("q-bio.QM", "protein structure prediction", "computational-biology", 4),
    ("q-bio.BM", "molecular dynamics simulation", "computational-biology", 4),
    ("physics.comp-ph", "numerical simulation", "scientific-computing", 3),
    ("stat.ML", "bayesian inference", "scientific-computing", 3),
]

# JOSS CrossRef queries (broad, recent)
JOSS_QUERIES = ["python", "machine learning", "genomics", "astronomy", "physics"]
JOSS_PER_QUERY = 3


def esc(s: str) -> str:
    """Quote a frontmatter string value."""
    return '"' + str(s).replace('"', "'").replace("\n", " ").strip() + '"'


def write_paper(
    *,
    filename: str,
    title: str,
    authors: list[str],
    year: int | None,
    source: str,
    source_id: str,
    url: str,
    domain: str,
    text: str,
) -> bool:
    """Write a single paper's text + frontmatter to the corpus directory.

    :param filename: Output filename (without directory).
    :param title: Paper title.
    :param authors: Author names.
    :param year: Publication year (if known).
    :param source: ``"arxiv"`` or ``"joss"``.
    :param source_id: arXiv ID or DOI.
    :param url: Canonical URL.
    :param domain: Subject domain.
    :param text: Full extracted text.
    :returns: ``True`` if the file was written.
    """
    if not text or len(text.strip()) < 200:
        return False
    # Strip NULs and stray control chars that pymupdf emits from some PDFs.
    text = text.replace("\x00", "")
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", text)
    body = re.sub(r"\n{3,}", "\n\n", text.strip())
    authors_str = ", ".join(authors[:12]) if authors else "Unknown"
    frontmatter = "\n".join(
        [
            "---",
            f"title: {esc(title)}",
            f"authors: {esc(authors_str)}",
            f"year: {year if year else ''}",
            f"source: {source}",
            f"source_id: {esc(source_id)}",
            f"url: {esc(url)}",
            f"domain: {domain}",
            "---",
            "",
        ]
    )
    out = OUTPUT_DIR / filename
    out.write_text(frontmatter + body + "\n", encoding="utf-8")
    return True


def fetch_arxiv() -> int:
    """Search arXiv, download PDFs, extract full text. Returns count written."""
    client = arxiv.Client()
    written = 0
    seen: set[str] = set()
    for cat, terms, domain, n in ARXIV_PULLS:
        query = f"cat:{cat} AND all:{terms}"
        print(f"[arxiv] {query} (n={n})")
        try:
            search = arxiv.Search(
                query=query, max_results=n, sort_by=arxiv.SortCriterion.Relevance
            )
            results = list(client.results(search))
        except Exception as exc:  # noqa: BLE001
            print(f"  search failed: {exc!r}")
            continue
        for r in results:
            arxiv_id = r.entry_id.split("/abs/")[-1].split("v")[0]
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)
            try:
                pdf_bytes = requests.get(
                    r.pdf_url, timeout=60, headers={"User-Agent": UA}
                ).content
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                text = "\n".join(page.get_text() for page in doc)
                year = r.published.year if r.published else None
                ok = write_paper(
                    filename=f"arxiv_{arxiv_id.replace('/', '_')}.md",
                    title=r.title,
                    authors=[str(a) for a in r.authors],
                    year=year,
                    source="arxiv",
                    source_id=arxiv_id,
                    url=r.entry_id,
                    domain=domain,
                    text=text,
                )
                if ok:
                    written += 1
                    print(f"  + arxiv_{arxiv_id} ({len(text)} chars) [{domain}]")
                time.sleep(1.0)  # be polite to arXiv
            except Exception as exc:  # noqa: BLE001
                print(f"  ! {arxiv_id} failed: {exc!r}")
    return written


def _clean_joss_html(html: str) -> str:
    """Extract the paper body from a joss.theoj.org page, strip chrome."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "form"]):
        tag.decompose()
    root = soup.find("article") or soup.find(id="paperd") or soup
    txt = root.get_text("\n")
    # Cut tail chrome
    for marker in ["Table of Contents", "Public user content licensed", "ISSN"]:
        idx = txt.find(marker)
        if idx > 200:
            txt = txt[:idx]
    return re.sub(r"\n{3,}", "\n\n", txt).strip()


def fetch_joss() -> int:
    """Get published JOSS DOIs via CrossRef, fetch each paper page."""
    written = 0
    seen: set[str] = set()
    for q in JOSS_QUERIES:
        print(f"[joss] crossref query={q!r}")
        try:
            resp = requests.get(
                "https://api.crossref.org/works",
                params={
                    "filter": "prefix:10.21105,type:journal-article,from-pub-date:2023-01-01",
                    "query": q,
                    "rows": JOSS_PER_QUERY,
                    "select": "DOI,title,author,published",
                },
                timeout=30,
                headers={"User-Agent": UA},
            )
            items = resp.json()["message"]["items"]
        except Exception as exc:  # noqa: BLE001
            print(f"  crossref failed: {exc!r}")
            continue
        for it in items:
            doi = it["DOI"]
            if doi in seen:
                continue
            seen.add(doi)
            title = (it.get("title") or ["Untitled"])[0]
            authors = [
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in it.get("author", [])
            ]
            year = (it.get("published", {}) or {}).get("date-parts", [[None]])[0][0]
            try:
                page = requests.get(
                    f"https://joss.theoj.org/papers/{doi}",
                    timeout=30,
                    headers={"User-Agent": UA},
                )
                text = _clean_joss_html(page.text) if page.status_code == 200 else ""
                ok = write_paper(
                    filename=f"joss_{doi.replace('/', '_').replace('.', '_')}.md",
                    title=title,
                    authors=authors,
                    year=year,
                    source="joss",
                    source_id=doi,
                    url=f"https://joss.theoj.org/papers/{doi}",
                    domain="software",
                    text=text,
                )
                if ok:
                    written += 1
                    print(f"  + joss {doi} ({len(text)} chars)")
                time.sleep(0.5)
            except Exception as exc:  # noqa: BLE001
                print(f"  ! joss {doi} failed: {exc!r}")
    return written


def main() -> None:
    """Fetch all arXiv + JOSS papers and write them to the corpus directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    n_arxiv = fetch_arxiv()
    n_joss = fetch_joss()
    total = len(list(OUTPUT_DIR.glob("*.md")))
    print(f"\nDONE: arxiv={n_arxiv} joss={n_joss} | total files in corpus: {total}")
    if total < 30:
        print("WARNING: fewer than 30 papers — re-run or widen queries.")


if __name__ == "__main__":
    main()
