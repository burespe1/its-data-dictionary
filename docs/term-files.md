# Term files

One Markdown file per term in `terms/<regulation>/<id>.md`. The file name is the `id`.

A term file is the full record of the entry agreed in the Word template: YAML front matter for the fields that are short and structured, Markdown sections for the explanatory content, including figures and code examples. The SKOS file (`itsdd.ttl`) is generated from it and holds only the part SKOS is made for.

## Front matter

| Field | Required | Content | In the Turtle |
| --- | --- | --- | --- |
| `id` | yes | Stable identifier, lower case with hyphens; never changed or reused | concept URI |
| `label` | yes | Name as in the legal text | `skos:altLabel` (or `skos:prefLabel` if there is no short name) |
| `short_name` | no | Short, content-based name | `skos:prefLabel` |
| `definition` | yes for `approved` | Concise definition | `skos:definition` |
| `category`, `subcategory` | no | Position in the annex of the regulation | – |
| `language` | no | `en` | language tag |
| `status` | yes | `proposed`, `ready for review`, `under review`, `approved`, `for thorough review`, `archived` | `owl:deprecated` when archived |
| `source` | yes | Legal act, e.g. `DR_EU_2022-670` | `r5r:applicableLegislation` (ELI) |
| `modes` | no | List of relevant transport modes | – |
| `mobility_theme` | no | List of mobilityDCAT-AP mobility-theme URIs | `skos:closeMatch` |
| `model` | no | Link to a detailed concept model (SKOS models repository) | `rdfs:seeAlso` |
| `created`, `modified` | no | Dates (YYYY-MM-DD) of first and last approval; set by the maintainer at release | `dct:modified` |
| `note` | no | Status note, e.g. the successor of an archived term | – |

There is no per-term version number: the release carries the version, the term carries `modified`.

## Body

Sections in this order, each optional:

```markdown
## Related standards
## Best practices
## Correspondence with Transmodel/NeTEx concepts   (or DATEX II, …)
## Example
## References
## Data quality
```

Figures go to `terms/assets/img/` and are linked as `![Figure 1](../assets/img/<id>-1.png)`. Code examples are fenced blocks with a language (`xml`, `json`); longer ones may go to `terms/assets/code/`.

## Example

```markdown
---
id: road-classification
label: road classification
definition: the minimum information required for distinguishing the links of a road network encompassing form of way, functional, or other concerns.
category: Types of data on infrastructure
language: en
status: proposed
source: DR_EU_2022-670
mobility_theme:
  - https://w3id.org/mobilitydcat-ap/mobility-theme/road-classification
---

## Best practices

According to ETSI TS 102 894-2 (DE=RoadType), road types are distinguished …

![Figure 1](../assets/img/road-classification.png)
```
