# NAPCORE ITS Data Dictionary

[![Release](https://img.shields.io/github/v/release/NAPCORE/its-data-dictionary?filter=itsdd-v*&label=release&style=flat-square)](https://github.com/NAPCORE/its-data-dictionary/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/NAPCORE/its-data-dictionary/build.yml?branch=main&label=build&style=flat-square)](https://github.com/NAPCORE/its-data-dictionary/actions/workflows/build.yml)
[![Website](https://img.shields.io/badge/website-release%20%7C%20draft-blue?style=flat-square)](https://napcore.github.io/its-data-dictionary/)
[![SKOS](https://img.shields.io/badge/SKOS-itsdd.ttl-blue?style=flat-square)](https://napcore.github.io/its-data-dictionary/itsdd.ttl)
[![Terms](https://img.shields.io/endpoint?style=flat-square&url=https%3A%2F%2Fnapcore.github.io%2Fits-data-dictionary%2Fdraft%2Fbadges%2Fterms.json)](https://napcore.github.io/its-data-dictionary/draft/all-terms/)
[![Approved](https://img.shields.io/endpoint?style=flat-square&url=https%3A%2F%2Fnapcore.github.io%2Fits-data-dictionary%2Fdraft%2Fbadges%2Fapproved.json)](https://napcore.github.io/its-data-dictionary/draft/all-terms/)
[![Open comments](https://img.shields.io/github/issues/NAPCORE/its-data-dictionary/review?label=open%20comments&style=flat-square)](https://github.com/NAPCORE/its-data-dictionary/issues?q=is%3Aissue+is%3Aopen+label%3Areview)
[![License](https://img.shields.io/github/license/NAPCORE/its-data-dictionary?style=flat-square)](LICENSE)

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
python scripts/build.py && zensical serve -f mkdocs.gen.yml # preview the website locally
```

See [docs/workflow.md](docs/workflow.md) for the release steps and [docs/term-files.md](docs/term-files.md) for the fields of a term file.

## License

See [LICENSE](LICENSE).
