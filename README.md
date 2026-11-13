# NAPCORE ITS Data Dictionary

Definitions of the data categories in the delegated regulations of the ITS Directive (MMTIS, RTTI, SRTI, SSTP), AFIR and TEL-TSI, maintained by NAPCORE Task 5.3.1.

**Readers:** use the website (GitHub Pages of this repository): the latest release at the root, work in progress under `/draft/`, all terms with their status on the page *All terms*. Select any text on a page to comment on it; this opens a short GitHub issue form.

**Machines:** the SKOS vocabulary is published with every release as `itsdd.ttl`. Its URIs are provisional until the namespace is decided.

## How the content gets here

The definitions are drafted and agreed in the Word working document of Task 5.3.1. After a release is approved, the repository maintainer converts the Word document into the term files of this repository with `scripts/word2md.py`. Nothing in this repository is edited by experts directly, and nothing generated is committed.

Detailed SKOS concept models (for example NAPCORE Core Concepts) are published separately in [its-data-dictionary-skos-models](https://github.com/NAPCORE/its-data-dictionary-skos-models).

## Repository layout

```text
terms/<regulation>/<id>.md   one file per term: YAML front matter + Markdown body
terms/assets/                figures and code examples used by term files
scripts/word2md.py           Word consolidation document -> term files
scripts/build.py             term files -> website sources and itsdd.ttl
docs/                        how term files are written and how releases work
archive/phase1-source/       the NAPCORE Phase 1 dictionary as published in 2024
```

Regulation folders: `2024-490` MMTIS, `2022-670` RTTI, `886-2013` SRTI, `885-2013` SSTP, `2023-1804` AFIR, `2026-253` TEL-TSI, `2015-962` RTTI (repealed, archived terms).

## For the maintainer

```bash
pip install -r scripts/requirements.txt
python scripts/word2md.py CONSOLIDATION.docx --out _import   # convert and compare, writes _import/REPORT.md
python scripts/build.py --check                              # validate term files
python scripts/build.py && mkdocs serve -f mkdocs.gen.yml   # preview the website locally
```

See [docs/workflow.md](docs/workflow.md) for the release steps and [docs/term-files.md](docs/term-files.md) for the fields of a term file.

## License

See [LICENSE](LICENSE).
