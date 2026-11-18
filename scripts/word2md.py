"""Convert the Word consolidation document of the ITS Data Dictionary into term files.

Every entry in the Word document is a two-column table that starts with a "Name" row
(the template agreed in Prague). The regulation and category of an entry are taken from
the headings above the table.

Usage:
    python scripts/word2md.py CONSOLIDATION.docx                 # dry run: report only
    python scripts/word2md.py CONSOLIDATION.docx --out _import   # write term files to _import/
    python scripts/word2md.py CONSOLIDATION.docx --out terms     # overwrite the term files

The default is a dry run, so the repository is never changed by accident.
Requires: python-docx, PyYAML.
"""
import argparse
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import docx
import yaml
from docx.table import Table
from docx.text.paragraph import Paragraph

# Heading 1 text in the Word document -> folder under terms/ and source code
REGULATIONS = {
    "MMTIS": ("2024-490", "DR_EU_2024-490"),
    "RTTI": ("2022-670", "DR_EU_2022-670"),
    "SRTI": ("886-2013", "DR_EU_886-2013"),
    "SSTP": ("885-2013", "DR_EU_885-2013"),
    "AFIR": ("2023-1804", "REG_EU_2023-1804"),
    "TEL-TSI": ("2026-253", "REG_IMPL_EU_2026-253"),
}

# Template rows -> where they go. Front matter keys or body section titles.
FRONT = {"name": "label", "short name": "short_name", "id": "id", "definition": "definition"}
LIST_FIELDS = {"relevant modes": "modes", "mobilitydcat-ap correspondence": "mobility_theme"}
SKIP = {"version"}  # replaced by release version + `modified` (see docs/workflow.md)
BODY_ORDER = ["related standards", "best practices", "correspondence", "example",
              "references/additional info", "data quality"]
BODY_TITLES = {"related standards": "Related standards", "best practices": "Best practices",
               "example": "Example", "references/additional info": "References",
               "data quality": "Data quality"}

CODE_HINT = re.compile(r"^\s*(<\?xml|<[A-Za-z][\w:.-]*[\s>]|\{\s*\"|\[\s*\{)")


def slug(text, maxlen=60):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"\([^)]*\)", "", text)          # drop bracketed examples
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:maxlen].rstrip("-") or "term"


def clean(text):
    lines = [l.rstrip() for l in text.replace("\r", "").split("\n")]
    out, blank = [], 0
    for l in lines:
        blank = blank + 1 if not l.strip() else 0
        if blank < 2:
            out.append(l)
    return "\n".join(out).strip()


def as_markdown(text):
    """Keep plain text; fence anything that looks like code (XML, JSON)."""
    text = clean(text)
    if CODE_HINT.match(text):
        lang = "xml" if text.lstrip().startswith("<") else "json"
        return f"```{lang}\n{text}\n```"
    return text


def cell_text(cell, skip_first=False):
    """Cell text in Markdown: list paragraphs become bullets, nested tables become Markdown tables.
    With skip_first, the first non-empty paragraph (the definition itself) is left out."""
    out, skipped = [], not skip_first
    for el in cell._tc.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, cell)
            t = p.text.strip()
            if not skipped:
                if t:
                    skipped = True
                continue
            ppr = p._p.pPr
            is_list = (ppr is not None and ppr.numPr is not None) or \
                (p.style is not None and "list" in p.style.name.lower())
            out.append(f"- {t}" if (is_list and t) else t)
        elif tag == "tbl" and skipped:
            rows = [[c.text.strip().replace("\n", " ").replace("|", "\\|") for c in r.cells]
                    for r in Table(el, cell).rows]
            if rows:
                out.append("")
                out.append("| " + " | ".join(rows[0]) + " |")
                out.append("|" + " --- |" * len(rows[0]))
                out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                out.append("")
    return "\n".join(out)


def first_paragraph(cell):
    """The definition: the first non-empty paragraph of the Definition cell."""
    for p in cell.paragraphs:
        if p.text.strip():
            return clean(p.text)
    return ""


def cell_images(cell, doc, prefix, outdir):
    """Extract pictures in a table cell; return relative markdown image links."""
    links = []
    blips = cell._element.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
    for n, blip in enumerate(blips, 1):
        rid = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
        if not rid or rid not in doc.part.related_parts:
            continue
        part = doc.part.related_parts[rid]
        ext = Path(part.partname).suffix or ".png"
        name = f"{prefix}-{n}{ext}"
        if outdir is not None:
            (outdir / "assets" / "img").mkdir(parents=True, exist_ok=True)
            (outdir / "assets" / "img" / name).write_bytes(part.blob)
        links.append(f"![Figure {n}](../assets/img/{name})")
    return links


def walk(doc):
    """Yield (headings, table) for every entry table, with the heading path above it."""
    headings, reg = {}, None
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, doc)
            style = p.style.name if p.style is not None else ""
            m = re.match(r"Heading (\d)", style)
            if m and p.text.strip():
                lvl = int(m.group(1))
                text = p.text.strip()
                if lvl == 1:
                    found = next((k for k in REGULATIONS if text.upper().startswith(k)), None)
                    if found or "GLOSSARY" in text.upper() or text.lower().startswith("structure"):
                        reg = None if (not found or "GLOSSARY" in text.upper()) else found
                        headings = {}
                        continue
                headings = {k: v for k, v in headings.items() if k < lvl}
                headings[lvl] = text
        elif tag == "tbl":
            t = Table(el, doc)
            try:
                first = t.rows[0].cells
            except IndexError:
                continue
            if len(first) == 2 and first[0].text.strip() == "Name" \
                    and first[1].text.strip() != "Name of the category":
                yield reg, dict(headings), t



def convert(path, outdir=None):
    doc = docx.Document(path)
    entries, problems, placeholders = [], [], []
    seen = Counter()
    for reg, headings, table in walk(doc):
        if reg is None:
            if not table.rows[0].cells[1].text.strip():
                continue  # blank template table at the top of the document
            problems.append(("?", "entry before any regulation heading", table.rows[0].cells[1].text[:60]))
            continue
        folder, source = REGULATIONS[reg]
        rows = {}
        for r in table.rows:
            cells = r.cells
            if len(cells) < 2:
                continue
            key = clean(cells[0].text).split("\n")[0].strip().lower()
            rows.setdefault(key, (clean(cells[0].text), cells[1]))
        name = clean(rows["name"][1].text)
        short = clean(rows["short name"][1].text) if "short name" in rows else ""
        if not name and not short:
            where = headings[max(headings)] if headings else "?"
            placeholders.append((folder, where))
            continue
        name = name or short
        given_id = clean(rows["id"][1].text) if "id" in rows else ""
        term_id = given_id or slug(short or name)
        seen[(folder, term_id)] += 1
        if seen[(folder, term_id)] > 1:
            term_id = f"{term_id}-{seen[(folder, term_id)]}"
        fm = {"id": term_id, "label": name}
        if short:
            fm["short_name"] = short
        fm["definition"] = first_paragraph(rows["definition"][1]) if "definition" in rows else ""
        path_h = [headings[k] for k in sorted(headings)]
        if path_h:
            fm["category"] = path_h[0]
        if len(path_h) > 1:
            fm["subcategory"] = path_h[1:-1] if path_h[-1] == name else path_h[1:]
        fm["language"] = "en"
        fm["status"] = "proposed"
        fm["source"] = source
        body, missing = [], []
        for key, (label, cell) in rows.items():
            if key in FRONT or key in SKIP:
                continue
            text = clean(cell.text)
            if key in LIST_FIELDS:
                vals = [v.strip() for v in re.split(r"[;\n,]", text) if v.strip()]
                if vals:
                    fm[LIST_FIELDS[key]] = vals
                continue
        if "definition" in rows:  # explanation that follows the definition in the same cell
            dcell = rows["definition"][1]
            text = as_markdown(cell_text(dcell, skip_first=True))
            imgs = cell_images(dcell, doc, f"{term_id}-def", (outdir / folder).parent if outdir else None)
            if text or imgs:
                body.append("## Explanation\n\n" + "\n\n".join([t for t in [text] if t] + imgs))
        for wanted in BODY_ORDER:
            for key, (label, cell) in rows.items():
                if not (key == wanted or (wanted == "correspondence" and key.startswith("correspondence"))):
                    continue
                text = as_markdown(cell_text(cell))
                imgs = cell_images(cell, doc, f"{term_id}", (outdir / folder).parent if outdir else None)
                if not text and not imgs:
                    missing.append(BODY_TITLES.get(key, label))
                    continue
                title = BODY_TITLES.get(key, label.split("\n")[0])
                body.append(f"## {title}\n\n" + "\n\n".join([t for t in [text] if t] + imgs))
        if not fm["definition"]:
            problems.append((folder, "no definition", name[:60]))
        entries.append({"folder": folder, "fm": fm, "body": body, "missing": missing,
                        "given_id": bool(given_id)})
    return entries, problems, placeholders


def write(entries, outdir):
    for e in entries:
        target = outdir / e["folder"] / f"{e['fm']['id']}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        head = yaml.safe_dump(e["fm"], sort_keys=False, allow_unicode=True, width=1000)
        text = f"---\n{head}---\n\n" + "\n\n".join(e["body"]) + "\n"
        target.write_text(text, encoding="utf-8")


def existing_labels(terms_dir):
    found = {}
    for f in Path(terms_dir).glob("*/*.md"):
        m = re.search(r"^label:\s*(.+)$", f.read_text(encoding="utf-8"), re.M)
        if m:
            found[m.group(1).strip().strip('"').lower()] = f
    return found


def report(entries, problems, placeholders, terms_dir):
    per = Counter(e["folder"] for e in entries)
    known = existing_labels(terms_dir) if terms_dir and Path(terms_dir).exists() else {}
    matched = sum(1 for e in entries if e["fm"]["label"].lower() in known)
    lines = ["# word2md report", "", f"Entries found: {len(entries)}", ""]
    lines += ["| Regulation folder | Entries |", "| --- | --- |"]
    lines += [f"| {k} | {v} |" for k, v in sorted(per.items())]
    lines += ["", f"Entries with an ID in Word: {sum(e['given_id'] for e in entries)}",
              f"Entries whose label matches an existing term file: {matched}", ""]
    empty = Counter(m for e in entries for m in e["missing"])
    if empty:
        lines += ["Empty template fields (number of entries):", ""]
        lines += [f"- {k}: {v}" for k, v in empty.most_common()]
    if placeholders:
        lines += ["", f"Empty entry tables, not converted ({len(placeholders)}):", ""]
        lines += [f"- {a}: {b}" for a, b in placeholders]
    if problems:
        lines += ["", "Problems:", ""] + [f"- {a}: {b} ({c})" for a, b, c in problems]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--out", help="folder to write term files to (omit for a dry run)")
    ap.add_argument("--terms", default="terms", help="existing term folder, for the comparison in the report")
    args = ap.parse_args()
    outdir = Path(args.out) if args.out else None
    entries, problems, placeholders = convert(args.docx, outdir)
    rep = report(entries, problems, placeholders, args.terms)
    if outdir:
        write(entries, outdir)
        (outdir / "REPORT.md").write_text(rep, encoding="utf-8")
    sys.stdout.write(rep)


if __name__ == "__main__":
    main()
