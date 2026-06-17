# Editing this site

## Easiest: the browser editor

For papers, awards, and news, just run:

```bash
python scripts/editor.py
```

It opens a local page (http://localhost:8777) with tabs to add, edit, reorder,
and delete entries — no syntax to remember. Papers auto-fill title/authors from
an arXiv id. It only changes your local files; preview with `hugo server` and
commit when you're happy. Press Ctrl+C to stop it. The manual steps below still
work if you prefer editing files directly.

---

Quick reference for the most common updates. Preview everything locally with:

```bash
hugo server -D
```

---

## Add a paper

Easiest — use the helper script (auto-fills title/authors/abstract from arXiv):

```bash
# A preprint / under-review paper:
python scripts/add_publication.py --arxiv 2505.20177 \
    --topic "Testable Learning" --status preprint

# A peer-reviewed paper:
python scripts/add_publication.py --arxiv 2401.12345 \
    --topic "Learning with Distribution Shift" \
    --status published --venue "NeurIPS 2024"

# With a distinction badge:
python scripts/add_publication.py --arxiv 2401.12345 \
    --topic "Testable Learning" --status published --venue "COLT 2024" \
    --award "Best Paper Award · COLT 2024"
```

No arXiv id? Provide the fields by hand:

```bash
python scripts/add_publication.py \
    --title "My Paper" --authors "Jane Doe; Konstantinos Stavropoulos; John Roe" \
    --year 2025 --topic "Other" --status preprint \
    --abstract "We show that ..." --url https://arxiv.org/abs/2501.00001
```

What the flags do:

- `--status published` → `featured: true`. Appears in **Selected** (under its
  area) and in **All** (under Published).
- `--status preprint` → `featured: false`. Appears only in **All** (under Preprints).
- `--topic` → the research area for the Selected view (see list below).
- Your name is automatically replaced with `admin` so it's bolded.

Run `python scripts/add_publication.py -h` for all options.

### Or do it by hand
Each paper is a folder under `content/publication/<slug>/` with an `index.md`.
Copy an existing one and edit the front matter. The fields that matter:

```yaml
featured: true            # true = published (Selected + All); false = preprint
categories:
- Testable Learning       # research area (used by the Selected view)
publication: '*NeurIPS 2024*'   # venue, or '*Under review*'
award: 'Best Paper Award · COLT 2024'   # optional — shows a colored badge
links:
- name: URL               # the card title links to this URL (arXiv abs page)
  url: https://arxiv.org/abs/2501.00001
url_pdf: https://arxiv.org/pdf/2501.00001   # adds a small "PDF" button
```

Each paper renders as a **card** (authors / title / venue, plus the award
badge if set). Clicking the title opens the `URL` link (arXiv abs). There are
**no separate per-paper pages** — that's disabled in
`content/publication/_index.md`.

---

## How the Publications section works
One block (`id: publications`) renders a **Selected / All** toggle. The logic
lives in `layouts/partials/blocks/collection.html`; one card is drawn by
`layouts/partials/pub_card.html`; styling is in `assets/scss/custom.scss`.

- **Selected** — published papers grouped by research **area**.
- **All** — every paper by date (newest first): Published, then Preprints.

### The research areas (Selected view)
Defined in `data/areas.yaml` — each area has a `title` and a 2-3 sentence
`description` shown above a collapsible list of its papers:

```yaml
- title: Learning with Distribution Shift
  description: >-
    Two or three sentences about this line of work.
```

A paper's area is the first value of its `categories:` field, which must match
an area `title`. Use `Other` (or anything not listed) to keep a published paper
out of Selected — it still shows in All. **To add/rename an area:** edit
`data/areas.yaml`, then tag papers with the matching `categories:` value.
The paper list under each area is collapsible (it defaults to open; to default
it closed, remove `open` from `<details class="pub-cat-details" open>` in
`layouts/partials/blocks/collection.html`).

## Reorder papers
Papers are sorted by a numeric `rank:` field (lowest first), with date as a
tiebreaker. The browser editor's **Papers** tab lets you reorder with the ▲ ▼
buttons and **Save order**. By hand: set `rank:` in each paper's `index.md`
(e.g. `rank: 1`, `rank: 2`, …). The same ranking applies everywhere a paper
appears — within its area in **Selected** and within Published/Preprints in
**All** — so one ordering controls them all.

## Move a paper to a different area
Edit the `categories:` field in that paper's `index.md`.

## Promote a preprint to published
In the paper's `index.md`: set `featured: true` and update
`publication: '*Venue Year*'`.

---

## Update the News section
Edit the `news` block near the top of `content/_index.md`. To add an item,
copy one line and put it at the **top** (newest first):

```html
<div class="news-item"><span class="news-date">Oct 2026</span><span class="news-body">Attending NeurIPS 2026 in San Diego — come say hi!</span></div>
```

Only the date and the body text need changing. Links use normal `<a href="...">`.

---

## Talks (recorded / YouTube)
Edit `data/talks.yaml`. Each entry is a recorded talk that links to its video:

```yaml
enable: false           # currently hidden; set to true once you have a few
items:
  - title: My Talk Title
    youtube: https://youtu.be/VIDEO_ID
```

Each talk shows as a card with the YouTube icon; clicking it opens the video.

## Service
Edit `data/service.yaml`:

```yaml
enable: true
reviewing: 'COLT 2026, STOC 2026, ...'   # one line of venues -> "Reviewing" card
tutorials:                               # optional; card hidden while empty
  - title: Workshop name
    detail: "Venue / co-organizers"      # optional second line
    date: 2026
```

## Hiding a section
Set `enable: false` at the top of `data/talks.yaml` or `data/service.yaml` to
hide that section completely (heading included). Set it back to `true` to show.

## CV
Replace `static/uploads/resume.pdf` with your latest PDF (keep the same name).
It's linked from the **Download CV** button in your bio, the CV icon under your
name, and the **CV** item in the top navigation.

---

## Awards
Awards are cards with a **Selected / More** toggle, driven by
`data/awards.yaml`. Each entry:

```yaml
- title: Apple Scholars in AI/ML PhD Fellowship
  date: '2025'
  selected: true        # true -> shows in "Selected"; every item shows in "More"
  url: https://...       # optional, makes the title a link
  description: One sentence. Markdown [links](https://...) are allowed.
```

Order top-to-bottom = display order. Paper-specific distinctions (best paper,
orals) live on the papers themselves via the `award:` field, so keep this list
for fellowships, scholarships, and similar honors.

## Easter egg
Clicking your name (the About heading) 5× quickly shows a photo overlay. It's
theme-aware: `static/uploads/greece.jpg` (with a "Καλημέρα" caption) in light
mode, and `static/uploads/greece-night.jpg` (a "Καληνύχτα" caption) in dark
mode. The logic is `initEgg`/`showEgg` in
`layouts/partials/blocks/collection.html`; swap an image by replacing the file,
edit the captions in `showEgg`, or delete those two functions (and the
`initEgg()` call) to remove it.

## Styling
Visual tweaks live in `assets/scss/custom.scss` (accent color, spacing,
section headings, the News cards). Change the `--accent` color at the top to
recolor the whole site.
```
:root { --accent: #1f6feb; }
```
