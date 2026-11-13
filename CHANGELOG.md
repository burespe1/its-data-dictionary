# Changelog

One section per release, newest first. Tags: `itsdd-vX.Y.Z`.

## Unreleased

### Changed
- Repository simplified: term files moved from `drafts/DR_EU_*` to `terms/<regulation>/`; generated folders (`drafts/preview/`, `drafts/INDEX.md`, `release/`) and the hand-run scripts removed. The website and the Turtle are built by GitHub Actions.
- Three MMTIS terms with status `finalised` (not a defined status) set to `approved`: addresses, points of interest, topographic places.
- File `detailed-common--fare-query_common fare products.md` renamed to match its `id`.

### Added
- `scripts/word2md.py`: converts the Word consolidation document into term files and reports gaps.
- `scripts/build.py`: validates term files, builds the website sources and `itsdd.ttl`.
- Comment button on every web page and the issue form `review.yml`.

## 1.0.0

Phase 1 dictionary migrated to one file per term (tag `v1.0.0`).
