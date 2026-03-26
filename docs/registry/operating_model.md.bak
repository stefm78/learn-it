# Operating Model — Learn-it

## 1. Purpose

This repository is governed by pipelines.
It is not a free-form document repository anymore.

Its purpose is to:

- build canonical learning-system artifacts,
- validate structural and logical consistency,
- promote validated outputs into the current canonical state,
- preserve release history,
- isolate legacy materials from authoritative artifacts.

The governing rule is:

> We no longer work *inside files first*; we work *through an explicit pipeline*.

---

## 2. Scope

This operating model applies to all artifacts under the repository's formal production structure, in particular:

- `docs/registry/`
- `docs/pipelines/`
- `docs/prompts/shared/`
- `docs/patcher/shared/`
- `docs/cores/current/`
- `docs/cores/releases/`
- `docs/legacy/` and any preserved pre-framework materials

It governs how artifacts are created, modified, promoted, archived, and interpreted.

---

## 3. Source-of-truth hierarchy

### 3.1 Structural authority

Structural authority defines how the repository operates.

Authoritative locations:

- `docs/registry/`
- `docs/pipelines/`
- `docs/prompts/shared/`
- `docs/patcher/shared/`

These layers define:

- conventions,
- pipeline roles,
- shared prompting logic,
- shared patching and validation behavior.

### 3.2 Current canonical authority

Current canonical authority defines what is officially true *now*.

Authoritative files:

- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

These files are the current canonical state of the system.
They are authoritative for interpretation, downstream work, and future promotions.

### 3.3 Release authority

Release authority defines what has been officially published before.

Authoritative location:

- `docs/cores/releases/`

A release is an immutable historical snapshot.
A release may be superseded, but it must not be silently rewritten.

### 3.4 Non-authoritative reference layer

Non-authoritative materials may inform analysis, migration, or traceability, but they do not define the current system state.

Typical locations:

- `docs/legacy/`
- historical DSL documents,
- migration inputs,
- analysis notes,
- any preserved pre-pipeline artifacts.

Rule:

> Legacy may inform. Legacy does not govern.

---

## 4. Artifact statuses

Every important artifact should be interpretable through one of the following statuses:

- **WORKING** — work in progress, not authoritative
- **CANDIDATE** — pipeline output validated for review, not yet promoted
- **CURRENT** — current canonical authority
- **RELEASED** — official historical snapshot
- **LEGACY** — preserved reference, non-authoritative

If an artifact can be mistaken for canonical while not being canonical, it must be renamed, moved, marked, or archived.

---

## 5. Allowed change paths

All changes must enter through exactly one of the following operational paths.

### 5.1 Constitution path

Use this path when changing the semantic or structural content of the system, including:

- rules,
- constraints,
- parameters,
- dependency declarations,
- logical links,
- canonical model structure.

Pipeline:

- `constitution`

Expected result:

- validated working change,
- candidate artifact set,
- optional release promotion later.

### 5.2 Release path

Use this path when a validated candidate must become the new canonical repository state.

Pipeline:

- `release`

Expected result:

- promotion into `docs/cores/current/`,
- snapshot into `docs/cores/releases/`,
- traceable promotion event.

### 5.3 Migration path

Use this path when transforming or absorbing pre-framework or external materials.

Pipeline:

- `migration`

Expected result:

- transformed artifact,
- validation of transformed structure,
- handoff into constitution or release path when appropriate.

Rule:

> No parallel informal path may compete with `constitution`, `release`, or `migration`.

---

## 6. Manual edit policy

### 6.1 Allowed

Manual edits are allowed in:

- registry documents,
- pipeline documentation,
- shared prompts,
- shared patcher scripts,
- legacy markings,
- explanatory documentation.

### 6.2 Restricted

Direct manual edits to `docs/cores/current/` are restricted.

The canonical rule is:

- `current/` should normally be updated through a validated promotion path,
- not by ad hoc manual editing.

### 6.3 Emergency exception

A manual hotfix to `docs/cores/current/` is allowed only when all of the following are true:

- the issue is urgent,
- the correction is minimal and deterministic,
- the change is recorded,
- the source pipeline is regularized immediately afterward.

Rule:

> `current/` may be corrected exceptionally; it must not become a free-form editing zone.

### 6.4 Forbidden by default

The following are forbidden unless explicitly regularized:

- editing a release snapshot in place,
- using a legacy artifact as an authority source,
- bypassing pipeline intent while still claiming canonical status,
- keeping two apparently canonical versions of the same artifact without explicit status separation.

---

## 7. Standard lifecycle of a change

Every change should follow the same operational lifecycle.

### 7.1 Qualification

Classify the change:

- constitution,
- migration,
- release,
- or registry/governance maintenance.

### 7.2 Preparation

Identify:

- inputs,
- target pipeline,
- expected outputs,
- validation requirements,
- whether promotion is intended.

### 7.3 Execution

Run the relevant transformation, patching, or preparation logic.

### 7.4 Validation

Check at least:

- structural consistency,
- dependency coherence,
- invariant respect,
- release preconditions where applicable,
- naming and placement conventions.

### 7.5 Promotion

If and only if the result is intended to become authoritative:

- update `docs/cores/current/`,
- create a release snapshot,
- record the promotion.

### 7.6 Cleanup

Archive, mark, or relocate obsolete candidate or legacy materials to avoid ambiguity.

---

## 8. Release governance

A release is not merely a file copy.
It is a governance action that changes repository authority.

A valid release operation must do all of the following:

1. verify preconditions,
2. verify that the candidate set is internally coherent,
3. promote the candidate into `docs/cores/current/`,
4. write an immutable snapshot into `docs/cores/releases/`,
5. preserve traceability of the promotion event.

Rule:

> A release changes what is authoritative. It must therefore be explicit, reviewable, and reproducible.

---

## 9. Legacy policy

Legacy must be preserved deliberately, not allowed to float ambiguously near canonical material.

### 9.1 Legacy classes

#### A. Archive

Kept for traceability or historical reference.

#### B. Transitional compatibility

Kept temporarily because an existing workflow still depends on it.

#### C. Parasite

Accidental, duplicate, or misleading material that should be ignored or removed.

### 9.2 Legacy handling rule

Any visible legacy artifact that could be confused with canonical content must be:

- moved,
- clearly marked,
- or removed.

Recommended visible markers:

- `LEGACY`
- `NON_AUTHORITATIVE`
- `ARCHIVE_ONLY`

---

## 10. Registry responsibilities

`docs/registry/` is the declarative operating brain of the repository.

It should define and maintain at least:

### `conventions.md`

- naming rules,
- status vocabulary,
- authority rules,
- manual edit rules,
- legacy marking policy.

### `pipelines.md`

- pipeline roles,
- entry criteria,
- inputs,
- outputs,
- validations,
- promotion boundaries.

### `resources.md`

- inventory of shared prompts,
- inventory of patcher tools,
- inventory of shared resources,
- navigation guidance for contributors and automation.

### `operating_model.md`

- repository doctrine,
- source-of-truth hierarchy,
- change lifecycle,
- governance model,
- legacy and release policy.

---

## 11. Roles

This repository can be operated by one person or many, but the roles should still be conceptually separated.

### 11.1 Repository owner

Responsible for:

- approving structural changes,
- defining canonical promotion policy,
- deciding legacy handling,
- approving new pipelines or major governance changes.

### 11.2 Pipeline maintainer

Responsible for:

- shared script quality,
- patcher consistency,
- pipeline documentation quality,
- validation robustness,
- prompt and patch compatibility.

### 11.3 Contributor

Responsible for:

- classifying their change correctly,
- using the right path,
- not bypassing canonical governance,
- keeping non-authoritative artifacts clearly separated.

These roles may be performed by the same person, but they should not be confused conceptually.

---

## 12. Branching recommendation

The repository should keep a simple intention-based branching model.

### `main`

`main` must remain:

- coherent,
- readable,
- canonically interpretable,
- aligned with `docs/cores/current/`.

### Working branches

Recommended naming by intent:

- `constitution/...`
- `migration/...`
- `release/...`
- `governance/...`

Rule:

> One branch should have one dominant operational intent.

---

## 13. Definition of done

A change is done only when all of the following are true:

- the change path is identifiable,
- the artifact status is clear,
- the resulting files are placed in the correct authority layer,
- validation has been run where required,
- no ambiguous duplicate remains in a canonical-looking location,
- any release action is traceable,
- any affected governance documentation remains consistent.

---

## 14. Operational doctrine

The repository doctrine can be stated concisely as follows:

> Learn-it is governed by pipelines.
> `docs/cores/current/` contains the current canonical state.
> `docs/cores/releases/` contains historical promoted snapshots.
> `docs/registry/` defines how the repository is operated.
> Shared prompting and patching logic live in dedicated shared layers.
> Legacy informs but never governs.
> Any change that matters must follow an explicit operational path.

---

## 15. Immediate post-merge priorities

After framework merge, the operational priorities are:

1. keep `README.md` aligned with the actual repository authority structure,
2. mark or isolate legacy material that can cause canonical confusion,
3. harden release execution and validation so that promotion remains the normal trusted path,
4. ensure contributors and automation can identify the right authority layer without ambiguity.

---

## 16. Repository rule of interpretation

If two artifacts disagree, authority is resolved in this order:

1. current canonical core files,
2. release history,
3. registry-defined conventions and pipeline rules,
4. shared operational tooling,
5. legacy and historical references.

If ambiguity remains, the artifact with the clearer canonical status and the more recent explicit promotion wins.

