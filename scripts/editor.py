#!/usr/bin/env python3
"""
editor.py - a small local web app for editing this site's content.

Run it, open the page it prints, and use the forms to add / edit / reorder /
delete three things:

    * Papers  -> content/publication/<slug>/index.md  (+ cite.bib)
    * Awards  -> data/awards.yaml
    * News    -> the news block in content/_index.md

    python scripts/editor.py
    # then open http://localhost:8777  (it tries to open your browser for you)

Nothing is published anywhere. It only edits the local files; you still preview
with `hugo server` and decide when to commit / push. No third-party packages
are required (standard library only). Paper "add" reuses add_publication.py to
auto-fill title / authors from an arXiv id.
"""

import os
import re
import sys
import json
import html
import datetime
import threading
import webbrowser
import urllib.request
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PUB_DIR = os.path.join(ROOT, "content", "publication")
AWARDS_FILE = os.path.join(ROOT, "data", "awards.yaml")
AREAS_FILE = os.path.join(ROOT, "data", "areas.yaml")
INDEX_FILE = os.path.join(ROOT, "content", "_index.md")
PORT = int(os.environ.get("EDITOR_PORT", "8777"))
DEFAULT_ME = "Konstantinos Stavropoulos"

# Reuse the arXiv fetch + slug helpers from the existing add script.
sys.path.insert(0, HERE)
try:
    import add_publication as addpub  # noqa: E402
except Exception:  # pragma: no cover - fallback if the script is missing
    addpub = None


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def unquote_scalar(s):
    """Turn a YAML-ish scalar (maybe quoted) into a plain string."""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return s


def sq(s):
    """Emit a single-quoted YAML scalar."""
    return "'" + str(s).replace("'", "''") + "'"


def dq(s):
    """Emit a double-quoted YAML scalar."""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------
# AREAS (read-only: used to populate the topic dropdown)
# --------------------------------------------------------------------------
def read_areas():
    if not os.path.exists(AREAS_FILE):
        return []
    titles = []
    for line in read(AREAS_FILE).splitlines():
        m = re.match(r"^- title:\s*(.+?)\s*$", line)
        if m:
            titles.append(unquote_scalar(m.group(1)))
    return titles


# --------------------------------------------------------------------------
# PAPERS
# --------------------------------------------------------------------------
def split_front_matter(text):
    """Return (front_matter_text, body) for a '---' delimited file."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def fm_get(fm, key):
    m = re.search(r"(?m)^%s:[ \t]*(.+?)[ \t]*$" % re.escape(key), fm)
    return unquote_scalar(m.group(1)) if m else None


def fm_first_category(fm):
    m = re.search(r"(?m)^categories:[ \t]*\n[ \t]*-[ \t]*(.+?)[ \t]*$", fm)
    return unquote_scalar(m.group(1)) if m else None


def fm_links_url(fm):
    # first `url:` that lives under a `links:` block (not url_pdf)
    m = re.search(r"(?m)^links:[ \t]*\n(?:.*\n)*?[ \t]*url:[ \t]*(.+?)[ \t]*$", fm)
    return unquote_scalar(m.group(1)) if m else None


def venue_display(publication):
    if publication is None:
        return ""
    return publication.strip().strip("*").strip()


def read_papers(me=DEFAULT_ME):
    papers = []
    if not os.path.isdir(PUB_DIR):
        return papers
    for slug in sorted(os.listdir(PUB_DIR)):
        idx = os.path.join(PUB_DIR, slug, "index.md")
        if not os.path.isfile(idx):
            continue
        fm, _ = split_front_matter(read(idx))
        if fm is None:
            continue
        authors = re.findall(r"(?m)^[ \t]*-[ \t]*(.+?)[ \t]*$",
                             (re.search(r"(?m)^authors:[ \t]*\n((?:[ \t]*-[ \t]*.+\n)+)", fm)
                              or _Empty()).group(1) if re.search(r"(?m)^authors:", fm) else "")
        authors = [me if a.strip() == "admin" else a.strip() for a in authors]
        featured = (fm_get(fm, "featured") or "false").lower() == "true"
        rank_raw = fm_get(fm, "rank")
        try:
            rank = int(rank_raw) if rank_raw is not None else None
        except ValueError:
            rank = None
        papers.append({
            "slug": slug,
            "title": fm_get(fm, "title") or slug,
            "authors": authors,
            "date": fm_get(fm, "date") or "",
            "rank": rank,
            "featured": featured,
            "status": "published" if featured else "preprint",
            "category": fm_first_category(fm) or "",
            "venue": venue_display(fm_get(fm, "publication")),
            "award": fm_get(fm, "award") or "",
            "url": fm_links_url(fm) or "",
            "url_pdf": fm_get(fm, "url_pdf") or "",
        })
    # Show in the same order the site uses: rank ascending, date as a tiebreak.
    papers.sort(key=lambda p: p["date"], reverse=True)
    papers.sort(key=lambda p: p["rank"] if p["rank"] is not None else 10 ** 9)
    return papers


def _set_rank(fm, value):
    """Insert or replace the `rank:` line (kept right after `date:`)."""
    if re.search(r"(?m)^rank:.*$", fm):
        return re.sub(r"(?m)^rank:.*$", "rank: %d" % value, fm, count=1)
    if re.search(r"(?m)^date:.*\n", fm):
        return re.sub(r"(?m)^(date:.*\n)", r"\g<1>rank: %d\n" % value, fm, count=1)
    return "rank: %d\n" % value + fm


def reorder_papers(order):
    """order: list of slugs, top-to-bottom. Writes rank = 1..N to each."""
    for i, slug in enumerate(order, start=1):
        idx = os.path.join(PUB_DIR, slug, "index.md")
        if not os.path.isfile(idx):
            continue
        fm, body = split_front_matter(read(idx))
        if fm is None:
            continue
        fm = _set_rank(fm, i)
        write(idx, "---\n" + fm + "\n---\n" + body)
    return len(order)


class _Empty:
    def group(self, *_):
        return ""


def add_paper(data, me=DEFAULT_ME):
    """data: arxiv | (title, authors, year, url, pdf) + topic, status, venue, award."""
    if addpub is None:
        raise RuntimeError("add_publication.py not found next to editor.py")

    arxiv = (data.get("arxiv") or "").strip()
    if arxiv:
        meta = addpub.fetch_arxiv(arxiv)
        if data.get("title"):
            meta["title"] = data["title"]
    else:
        title = (data.get("title") or "").strip()
        authors = [a.strip() for a in re.split(r"[;\n]", data.get("authors", "")) if a.strip()]
        year = (data.get("year") or "").strip()
        if not (title and authors and year):
            raise ValueError("Without an arXiv id you must give title, authors and year.")
        meta = {
            "title": title, "abstract": data.get("abstract", ""),
            "authors": authors, "year": year, "date": "%s-01-01" % year,
            "url": data.get("url", ""), "pdf": data.get("pdf", ""),
        }
    if data.get("url"):
        meta["url"] = data["url"]
    if data.get("pdf"):
        meta["pdf"] = data["pdf"]

    status = data.get("status", "preprint")
    topic = data.get("topic") or "Other"
    venue = (data.get("venue") or "").strip()
    award = (data.get("award") or "").strip()

    # Build authors list with `admin` substitution.
    me_last = me.strip().split()[-1].lower()
    authors_out = ["admin" if a.split()[-1].lower() == me_last else a for a in meta["authors"]]

    featured = "true" if status == "published" else "false"
    if venue:
        publication = "*%s*" % venue
    elif status == "published":
        publication = "*Conference paper*"
    else:
        publication = "*Under review*"

    today = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    # New papers get rank 0 so they appear at the top until reordered.
    L = ["---", "title: " + sq(meta["title"]), "date: '%s'" % meta["date"],
         "rank: 0", "draft: false", "publishDate: '%s'" % today, "authors:"]
    L += ["- " + a for a in authors_out]
    L += ["publication_types:", "- 'paper-conference'", "categories:", "- " + topic]
    if meta.get("abstract"):
        L.append("abstract: " + sq(meta["abstract"]))
    L.append("featured: " + featured)
    if award:
        L.append("award: " + sq(award))
    L.append("publication: '%s'" % publication)
    if meta.get("pdf"):
        L.append("url_pdf: " + meta["pdf"])
    if meta.get("url"):
        L += ["links:", "- name: URL", "  url: " + meta["url"]]
    L += ["---", ""]

    slug = (data.get("slug") or "").strip() or addpub.slugify(
        "%s-%s-%s" % (addpub.last_name(meta["authors"][0]), meta["year"],
                      meta["title"].split()[0]))
    folder = os.path.join(PUB_DIR, slug)
    if os.path.exists(folder) and not data.get("force"):
        raise FileExistsError("A paper folder named '%s' already exists." % slug)
    os.makedirs(folder, exist_ok=True)
    write(os.path.join(folder, "index.md"), "\n".join(L))
    write(os.path.join(folder, "cite.bib"), addpub.build_bib(meta, slug))
    return slug


def edit_paper(data):
    """Surgically update only the changed front-matter fields of one paper."""
    slug = data["slug"]
    idx = os.path.join(PUB_DIR, slug, "index.md")
    if not os.path.isfile(idx):
        raise FileNotFoundError(slug)
    text = read(idx)
    fm, body = split_front_matter(text)
    if fm is None:
        raise ValueError("Could not parse front matter for %s" % slug)

    # title
    if "title" in data:
        fm = re.sub(r"(?m)^title:.*$", "title: " + sq(data["title"]), fm, count=1)
    # featured / status
    if "status" in data:
        feat = "true" if data["status"] == "published" else "false"
        if re.search(r"(?m)^featured:.*$", fm):
            fm = re.sub(r"(?m)^featured:.*$", "featured: " + feat, fm, count=1)
        else:
            fm = fm.rstrip("\n") + "\nfeatured: " + feat + "\n"
    # category (first item under categories:)
    if "category" in data and data["category"]:
        if re.search(r"(?m)^categories:[ \t]*\n[ \t]*-[ \t]*.+$", fm):
            fm = re.sub(r"(?m)^(categories:[ \t]*\n[ \t]*-[ \t]*).+$",
                        lambda m: m.group(1) + data["category"], fm, count=1)
        else:
            fm = fm.rstrip("\n") + "\ncategories:\n- " + data["category"] + "\n"
    # venue
    if "venue" in data:
        pub = "*%s*" % data["venue"].strip().strip("*").strip() if data["venue"].strip() else "*Under review*"
        if re.search(r"(?m)^publication:.*$", fm):
            fm = re.sub(r"(?m)^publication:.*$", "publication: '%s'" % pub, fm, count=1)
        else:
            fm = fm.rstrip("\n") + "\npublication: '%s'\n" % pub
    # award (add / change / remove)
    if "award" in data:
        if data["award"].strip():
            if re.search(r"(?m)^award:.*$", fm):
                fm = re.sub(r"(?m)^award:.*$", "award: " + sq(data["award"].strip()), fm, count=1)
            else:
                fm = re.sub(r"(?m)^(featured:.*\n)", r"\1award: " + sq(data["award"].strip()).replace("\\", "\\\\") + "\n", fm, count=1)
        else:
            fm = re.sub(r"(?m)^award:.*\n", "", fm, count=1)
    # primary URL (the link the title points to)
    if "url" in data and data["url"].strip():
        if re.search(r"(?m)^links:[ \t]*\n(?:.*\n)*?[ \t]*url:.*$", fm):
            fm = re.sub(r"(?m)^(links:[ \t]*\n(?:.*\n)*?[ \t]*url:[ \t]*).+$",
                        lambda m: m.group(1) + data["url"].strip(), fm, count=1)
        else:
            fm = fm.rstrip("\n") + "\nlinks:\n- name: URL\n  url: " + data["url"].strip() + "\n"
    # PDF URL
    if "url_pdf" in data:
        if data["url_pdf"].strip():
            if re.search(r"(?m)^url_pdf:.*$", fm):
                fm = re.sub(r"(?m)^url_pdf:.*$", "url_pdf: " + data["url_pdf"].strip(), fm, count=1)
            else:
                fm = re.sub(r"(?m)^(publication:.*\n)", r"\1url_pdf: " + data["url_pdf"].strip() + "\n", fm, count=1)
        else:
            fm = re.sub(r"(?m)^url_pdf:.*\n", "", fm, count=1)

    write(idx, "---\n" + fm + "\n---\n" + body)
    return slug


def delete_paper(slug):
    folder = os.path.join(PUB_DIR, slug)
    if not os.path.isdir(folder):
        raise FileNotFoundError(slug)
    for name in os.listdir(folder):
        os.remove(os.path.join(folder, name))
    os.rmdir(folder)


# --------------------------------------------------------------------------
# AWARDS (data/awards.yaml)
# --------------------------------------------------------------------------
AWARDS_HEADER = (
    "# Awards & achievements shown on the homepage.\n"
    "#   selected: true  -> appears in the \"Selected\" tab (highlights)\n"
    "#   every item      -> appears in the \"More\" tab\n"
    "# Order top-to-bottom = order shown. Markdown links are allowed in `description`.\n"
    "# Note: paper-specific distinctions (best paper, spotlight, oral) live on the\n"
    "#       papers themselves via the `award:` field, not here.\n"
    "# (This file is managed by scripts/editor.py, but is safe to hand-edit too.)\n\n"
)


def read_awards():
    items = []
    cur = None
    if not os.path.exists(AWARDS_FILE):
        return items
    for line in read(AWARDS_FILE).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^-[ \t]+(\w+):[ \t]*(.*)$", line)
        if m:
            if cur is not None:
                items.append(cur)
            cur = {"title": "", "date": "", "selected": False, "url": "", "description": ""}
            _set_award(cur, m.group(1), m.group(2))
            continue
        m = re.match(r"^[ \t]+(\w+):[ \t]*(.*)$", line)
        if m and cur is not None:
            _set_award(cur, m.group(1), m.group(2))
    if cur is not None:
        items.append(cur)
    return items


def _set_award(cur, key, val):
    val = val.strip()
    if key == "selected":
        cur["selected"] = val.lower() == "true"
    elif key in ("title", "date", "url", "description"):
        cur[key] = unquote_scalar(val)


def write_awards(items):
    out = [AWARDS_HEADER.rstrip("\n"), ""]
    for it in items:
        out.append("- title: " + dq(it.get("title", "")))
        out.append("  date: " + sq(str(it.get("date", ""))))
        out.append("  selected: " + ("true" if it.get("selected") else "false"))
        if (it.get("url") or "").strip():
            out.append("  url: " + it["url"].strip())
        out.append("  description: " + dq(it.get("description", "")))
        out.append("")
    write(AWARDS_FILE, "\n".join(out).rstrip("\n") + "\n")


# --------------------------------------------------------------------------
# NEWS (the news block inside content/_index.md)
# --------------------------------------------------------------------------
NEWS_ITEM_RE = re.compile(
    r'<div class="news-item">[ \t]*'
    r'<span class="news-date">(?P<date>.*?)</span>[ \t]*'
    r'<span class="news-body">(?P<body>.*?)</span>[ \t]*</div>',
    re.DOTALL)
NEWS_LIST_RE = re.compile(
    r'(?P<head><div class="news-list">\n)(?P<inner>.*?)(?P<tail>\n[ \t]*</div>\n[ \t]*\')',
    re.DOTALL)


def read_news():
    m = NEWS_LIST_RE.search(read(INDEX_FILE))
    if not m:
        return []
    return [{"date": d.strip().replace("''", "'"),
             "body": b.strip().replace("''", "'")}
            for d, b in NEWS_ITEM_RE.findall(m.group("inner"))]


def write_news(items):
    text = read(INDEX_FILE)
    m = NEWS_LIST_RE.search(text)
    if not m:
        raise RuntimeError("Could not find the news-list block in content/_index.md")
    lines = []
    for it in items:
        date = it.get("date", "").strip().replace("'", "''")
        body = it.get("body", "").strip().replace("'", "''")
        lines.append(
            '      <div class="news-item"><span class="news-date">%s</span>'
            '<span class="news-body">%s</span></div>' % (date, body))
    inner = "\n" + "\n\n".join(lines) + "\n"
    new = text[:m.start("inner")] + inner + text[m.end("inner"):]
    write(INDEX_FILE, new)


# --------------------------------------------------------------------------
# HTTP server
# --------------------------------------------------------------------------
def state():
    return {
        "me": DEFAULT_ME,
        "areas": read_areas(),
        "papers": read_papers(),
        "awards": read_awards(),
        "news": read_news(),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE, "text/html; charset=utf-8")
        if self.path == "/api/state":
            return self._json(200, state())
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except Exception as e:
            return self._json(400, {"error": "bad json: %s" % e})
        try:
            return self._route(self.path, data)
        except Exception as e:
            return self._json(400, {"error": str(e)})

    def _route(self, path, data):
        if path == "/api/arxiv":
            if addpub is None:
                raise RuntimeError("add_publication.py not found")
            meta = addpub.fetch_arxiv(data.get("arxiv", ""))
            return self._json(200, {"ok": True, "meta": meta})
        if path == "/api/paper/add":
            slug = add_paper(data)
            return self._json(200, {"ok": True, "slug": slug})
        if path == "/api/paper/edit":
            edit_paper(data)
            return self._json(200, {"ok": True})
        if path == "/api/paper/delete":
            delete_paper(data["slug"])
            return self._json(200, {"ok": True})
        if path == "/api/papers/reorder":
            n = reorder_papers(data["order"])
            return self._json(200, {"ok": True, "count": n})
        if path == "/api/awards/save":
            write_awards(data["awards"])
            return self._json(200, {"ok": True})
        if path == "/api/news/save":
            write_news(data["news"])
            return self._json(200, {"ok": True})
        return self._json(404, {"error": "unknown endpoint"})


# The web UI is defined in editor_page.py (kept separate so this file stays
# focused on file I/O). It is a single HTML string named PAGE.
from editor_page import PAGE  # noqa: E402


def main():
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://localhost:%d" % PORT
    print("\n  Site content editor running at:  %s" % url)
    print("  Editing files under:             %s" % ROOT)
    print("  Press Ctrl+C to stop.\n")
    try:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")


if __name__ == "__main__":
    main()
