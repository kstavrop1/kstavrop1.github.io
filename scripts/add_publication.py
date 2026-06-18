#!/usr/bin/env python3
"""
add_publication.py — create a new publication entry for the Hugo site.

It generates `content/publication/<slug>/index.md` (and a matching cite.bib),
filling in title, authors, abstract, links, the research-topic category, and
whether the paper is peer-reviewed (shown in a topic section) or a preprint
(shown in the "Preprints & Work in Progress" section).

QUICK START — from an arXiv id (auto-fetches title/authors/abstract):

    python scripts/add_publication.py --arxiv 2505.20177 \
        --topic "Testable Learning" --status preprint

    python scripts/add_publication.py --arxiv 2401.12345 \
        --topic "Learning with Distribution Shift" \
        --status published --venue "NeurIPS 2024"

FULLY MANUAL (no internet needed):

    python scripts/add_publication.py \
        --title "My Great Paper" \
        --authors "Jane Doe; Konstantinos Stavropoulos; John Roe" \
        --year 2025 --topic "Other Topics" --status preprint \
        --abstract "We show that ..." --url https://arxiv.org/abs/2501.00001

NOTES
  * Your own name is replaced with `admin` automatically (so the theme can
    highlight you). Change DEFAULT_ME below if needed, or pass --me "Your Name".
  * --topic is the research AREA used by the "Selected" view. Current areas
    (defined in layouts/partials/blocks/collection.html):
        Learning with Distribution Shift
        Learning with Noise
        Testable Learning
        Beyond Worst-Case Models
        Calibration and Real-Valued Prediction
    Use "Other" (or any string not in that list) for papers you don't want in
    the Selected view — they still appear in the "All" view by date.
    To add a new area, add it to the $areas list in collection.html.
  * --status published  -> featured: true  (appears in its topic section)
    --status preprint    -> featured: false (appears under Preprints)
  * Preview after running:  hugo server -D
"""

import argparse
import os
import re
import sys
import datetime
import urllib.request
import xml.etree.ElementTree as ET

DEFAULT_ME = "Konstantinos Stavropoulos"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_DIR = os.path.join(REPO_ROOT, "content", "publication")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def last_name(full_name):
    return full_name.strip().split()[-1] if full_name.strip() else "anon"


def fetch_arxiv(arxiv_id):
    """Return dict with title, authors (list), abstract, year, url, pdf."""
    arxiv_id = arxiv_id.strip().replace("arXiv:", "")
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = resp.read().decode("utf-8")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    entry = root.find("a:entry", ns)
    if entry is None:
        raise RuntimeError("No arXiv entry found for id " + arxiv_id)
    title = " ".join(entry.find("a:title", ns).text.split())
    abstract = " ".join(entry.find("a:summary", ns).text.split())
    authors = [a.find("a:name", ns).text.strip()
               for a in entry.findall("a:author", ns)]
    published = entry.find("a:published", ns).text  # e.g. 2025-05-26T...
    year = published[:4]
    date = published[:10]
    return {
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "year": year,
        "date": date,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf": f"https://arxiv.org/pdf/{arxiv_id}",
    }


def yaml_quote(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_index_md(meta, args):
    me = args.me or DEFAULT_ME
    me_last = last_name(me).lower()
    authors = []
    for a in meta["authors"]:
        if last_name(a).lower() == me_last:
            authors.append("admin")
        else:
            authors.append(a.strip())

    featured = "true" if args.status == "published" else "false"
    if args.venue:
        publication = f"*{args.venue}*"
    elif args.status == "published":
        publication = "*Conference paper*"
    else:
        publication = "*Preprint*"

    today = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z")

    lines = ["---"]
    lines.append(f"title: {yaml_quote(meta['title'])}")
    lines.append(f"date: '{meta['date']}'")
    lines.append("draft: false")
    lines.append(f"publishDate: '{today}'")
    lines.append("authors:")
    for a in authors:
        lines.append(f"- {a}")
    lines.append("publication_types:")
    lines.append("- 'paper-conference'")
    lines.append("categories:")
    lines.append(f"- {args.topic}")
    lines.append(f"abstract: {yaml_quote(meta['abstract'])}")
    lines.append(f"featured: {featured}")
    if args.award:
        lines.append(f"award: {yaml_quote(args.award)}")
    lines.append(f"publication: '{publication}'")
    if meta.get("pdf"):
        lines.append(f"url_pdf: {meta['pdf']}")
    if meta.get("url"):
        lines.append("links:")
        lines.append("- name: URL")
        lines.append(f"  url: {meta['url']}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_bib(meta, slug):
    authors = " and ".join(meta["authors"])
    entry_type = "article" if False else "inproceedings"
    fields = [
        f"  title = {{{meta['title']}}}",
        f"  author = {{{authors}}}",
        f"  year = {{{meta['year']}}}",
    ]
    if meta.get("url"):
        fields.append(f"  url = {{{meta['url']}}}")
    return f"@{entry_type}{{{slug},\n" + ",\n".join(fields) + "\n}\n"


def main():
    p = argparse.ArgumentParser(description="Add a publication to the Hugo site.")
    p.add_argument("--arxiv", help="arXiv id, e.g. 2505.20177 (auto-fetch).")
    p.add_argument("--title")
    p.add_argument("--authors", help='Semicolon-separated, e.g. "A B; C D".')
    p.add_argument("--abstract", default="")
    p.add_argument("--year")
    p.add_argument("--url", help="Landing URL (e.g. arXiv abs page).")
    p.add_argument("--pdf", help="Direct PDF URL.")
    p.add_argument("--venue", help='e.g. "NeurIPS 2024", "COLT 2025".')
    p.add_argument("--topic", required=True,
                   help="Research topic / category (must match a section).")
    p.add_argument("--status", required=True, choices=["published", "preprint"])
    p.add_argument("--award", help='Distinction badge, e.g. "Best Paper Award · COLT 2024".')
    p.add_argument("--me", help="Your full name (replaced with `admin`).")
    p.add_argument("--slug", help="Folder name override.")
    p.add_argument("--force", action="store_true",
                   help="Overwrite if the folder already exists.")
    args = p.parse_args()

    if args.arxiv:
        try:
            meta = fetch_arxiv(args.arxiv)
        except Exception as e:
            sys.exit(f"Could not fetch arXiv metadata: {e}\n"
                     f"Re-run with manual --title/--authors/--year instead.")
        # allow overrides
        if args.title:
            meta["title"] = args.title
        if args.abstract:
            meta["abstract"] = args.abstract
    else:
        if not (args.title and args.authors and args.year):
            sys.exit("Without --arxiv you must pass --title, --authors and --year.")
        meta = {
            "title": args.title,
            "abstract": args.abstract,
            "authors": [a.strip() for a in args.authors.split(";") if a.strip()],
            "year": args.year,
            "date": f"{args.year}-01-01",
            "url": args.url or "",
            "pdf": args.pdf or "",
        }
    if args.pdf:
        meta["pdf"] = args.pdf
    if args.url:
        meta["url"] = args.url

    slug = args.slug or slugify(
        f"{last_name(meta['authors'][0])}-{meta['year']}-{meta['title'].split()[0]}"
    )
    folder = os.path.join(PUB_DIR, slug)
    if os.path.exists(folder) and not args.force:
        sys.exit(f"Folder already exists: {folder}\nUse --force to overwrite "
                 f"or pass a different --slug.")
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "index.md"), "w") as f:
        f.write(build_index_md(meta, args))
    with open(os.path.join(folder, "cite.bib"), "w") as f:
        f.write(build_bib(meta, slug))

    print(f"Created {os.path.relpath(folder, REPO_ROOT)}/")
    print(f"  title : {meta['title']}")
    print(f"  topic : {args.topic}")
    print(f"  status: {args.status} (featured: "
          f"{'true' if args.status == 'published' else 'false'})")
    print("Preview with:  hugo server -D")


if __name__ == "__main__":
    main()
