# Workflow

## Where the work happens

| Step | Where | Who |
| --- | --- | --- |
| Draft and discuss definitions | Word working document (SharePoint) | Editors and experts of Task 5.3.1 |
| Approve a release package | Task 5.3.1, then the NAPCORE Steering Committee | Editors, SCOM |
| Transfer the approved text | this repository, `scripts/word2md.py` | Repository maintainer |
| Publish the website and Turtle | GitHub Actions (`.github/workflows/build.yml`) | automatic |
| Comment on published text | button on every web page → GitHub issue | anyone with a GitHub account |

## Release steps (repository maintainer)

1. Run `python scripts/word2md.py CONSOLIDATION.docx --out _import` and read `_import/REPORT.md`: entries per regulation, empty template fields, entries without a definition.
2. Copy the converted files from `_import/` into `terms/` in a branch. Keep existing `id`s; write new IDs back into the ID field of the Word template.
3. Set `status: approved` and `modified: <date>` on the terms that the release package approved, and `status: archived` with a `note` on terms that were withdrawn.
4. Run `python scripts/build.py --check`, open a pull request, let a second editor check the diff, merge.
5. Add a section to `CHANGELOG.md` and tag the merge commit `itsdd-vX.Y.Z`. The workflow builds and publishes the site and `itsdd.ttl`.

## Version numbers

Semantic Versioning for the dictionary as a whole:

- **MAJOR** – the meaning of an approved term changes, or an identifier changes.
- **MINOR** – terms are added, enriched without changing their meaning, or archived (they stay published as deprecated).
- **PATCH** – editorial corrections only.

Terms carry no version of their own, only the date of their last approved revision (`modified`). Terms are never deleted; an archived term keeps its file and its URI.

## Comments

The comment button on the website opens the issue form `.github/ISSUE_TEMPLATE/review.yml`, pre-filled with the term, the page and the selected text. The form asks whether a comment is editorial or substantive, which is also what decides the version number. During drafting, comments go into the Word working document as before.

## URIs

The namespace is not decided yet. Until then `build.py` writes provisional `https://example.org/provisional/itsdd/` URIs and says so in the file; set `ITSDD_BASE` once the namespace exists.
