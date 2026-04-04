# Platform Factory prompt family — transverse coherence review

## Scope reviewed

Prompt family reviewed as a governance chain:
- `docs/prompts/shared/Challenge_platform_factory.md`
- `tmp/Make21PlatformFactoryArbitrage.proposed.md`
- `tmp/Make22PlatformFactoryPatch.proposed.md`
- `tmp/Make23PlatformFactoryValidation.proposed.md`
- `tmp/Make24PlatformFactoryReview.proposed.md`

Reference governance documents reviewed:
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/pipelines/platform_factory/PROMPT_USAGE.md`

---

## Executive conclusion

The proposed prompt family is **globally strong and internally coherent**.

As a chain, it now enforces a much more disciplined progression:
- challenge identifies bounded and constitution-aware findings;
- arbitrage closes decisions and assigns the right treatment locus;
- patch synthesis translates only retained decisions into patch-ready changes;
- validation blocks drift both pre-apply and post-apply;
- final review evaluates true closeout, archive readiness and next-cycle cleanliness.

This is a clear improvement over the previous state.

However, the family is **not yet fully clean at repo level** for two reasons:
1. the repo currently mixes one already-updated live prompt (`Challenge_platform_factory.md`) with four proposed prompts still living only under `tmp/`;
2. there is a stage-map inconsistency between `pipeline.md` and `PROMPT_USAGE.md` around release materialization / promotion / closeout.

---

## Chain-by-chain coherence assessment

### 1. Challenge → Arbitrage
Status: **PASS**

The challenge prompt now produces the right kind of output for arbitrage:
- constitution-aware findings;
- distinction between acceptable V0 incompleteness and true governance defects;
- explicit likely correction loci;
- explicit issues around release/manifest/traceability;
- no premature patching.

The proposed arbitrage prompt correctly consumes one or more challenge reports and turns them into explicit decisions:
- retained now;
- rejected;
- deferred;
- clarification required;
- out of scope.

No major semantic gap detected.

### 2. Arbitrage → Patch
Status: **PASS**

The proposed patch prompt is correctly subordinated to arbitrage.
It does not reopen findings and explicitly forbids introducing non-arbitrated improvements.

The transition is strong because arbitrage now supplies:
- decision status;
- principal treatment locus;
- sequencing notes;
- patch preconditions.

Patch synthesis then translates that into:
- per-artifact change sets;
- probable localization;
- expected patch operation types;
- explicit exclusions from the current patchset.

This is the right level of determinism for a later patchset YAML.

### 3. Patch → Validation
Status: **PASS with one minor wording improvement suggested**

The proposed validation prompt is substantially improved because it now supports both:
- pre-apply patch validation;
- post-apply core validation.

This is exactly what the current pipeline needs from a reused validation prompt.

The patch prompt also explicitly emits what validation should later verify, which improves handoff quality.

Minor improvement suggested:
- in the validation output section, the wording `Conditions éventuelles avant promotion ou avant apply` could be made even more precise as:
  - `Conditions éventuelles avant apply, avant release materialization ou avant promotion`

This is not blocking, but it would align better with the repo’s stage model once that model is stabilized.

### 4. Validation → Review / Closeout
Status: **PASS**

The proposed review prompt is now aligned with a true closeout logic rather than a vague retrospective.
It correctly checks:
- stage coherence;
- quality of validations;
- materialization/promotion traceability;
- archive readiness;
- cleanliness for the next cycle.

This makes the family operationally coherent all the way to closeout.

---

## Residual repo-level inconsistencies

### A. Mixed live/proposed state of the prompt family
Severity: **high practical friction / low conceptual risk**

Current observed situation:
- `docs/prompts/shared/Challenge_platform_factory.md` is already updated in-place.
- `Make21/22/23/24` improved versions are still only under `tmp/`.

Impact:
- the family is coherent conceptually, but not yet coherent in the live repo state;
- an IA reading the live repo right now will still consume the old versions of Make21/22/23/24;
- this can produce inconsistent behavior across stages during a real run.

Required action:
- copy the four proposed prompts from `tmp/` into `docs/prompts/shared/`.

### B. Stage-map inconsistency between `pipeline.md` and `PROMPT_USAGE.md`
Severity: **high governance risk**

Observed inconsistency:
- `pipeline.md` currently presents a stage map ending at:
  - `STAGE_07_FACTORY_PROMOTION`
  - `STAGE_08_FACTORY_CLOSEOUT_AND_ARCHIVE`
- `PROMPT_USAGE.md` currently presents:
  - `STAGE_07_FACTORY_RELEASE_MATERIALIZATION`
  - `STAGE_08_FACTORY_PROMOTION`
  - `STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE`

Impact:
- any IA using the pipeline as the primary authority may reason on an 8-stage model;
- any IA using `PROMPT_USAGE.md` may reason on a 9-stage model with explicit release materialization;
- this ambiguity can leak into validation and closeout behavior;
- this weakens the credibility of the governance chain more than any individual prompt defect.

Required action:
- harmonize `docs/pipelines/platform_factory/pipeline.md` and `docs/pipelines/platform_factory/PROMPT_USAGE.md` onto the same stage map.

Recommended target:
- keep explicit separation between:
  - release materialization,
  - promotion,
  - closeout/archive.

That means the 9-stage model from `PROMPT_USAGE.md` is currently the more mature and governance-safe reference.

---

## Minor improvements suggested

### 1. Make23 output wording refinement
Severity: low

Suggested refinement in `tmp/Make23PlatformFactoryValidation.proposed.md`:
- replace `Conditions éventuelles avant promotion ou avant apply`
- with `Conditions éventuelles avant apply, avant release materialization ou avant promotion`

Rationale:
- better alignment with explicit release materialization staging.

### 2. Optional naming normalization across artifacts
Severity: low

The family is already coherent enough.
A future refinement could normalize a few recurring labels even further across prompts:
- `release governance`
- `manifest/release governance`
- `release / manifest / traçabilité`

This is not blocking and can be deferred.

---

## Overall verdict

### Prompt family coherence
Status: **PASS**

### Repo readiness to rely on this family in a real run
Status: **WARN**

Reason:
- the prompt family is strong, but the live repo still contains a mixed state and a stage-map inconsistency.

---

## Priority actions

### Priority 1
Apply the four proposed prompts from `tmp/` into `docs/prompts/shared/`.

### Priority 2
Harmonize `pipeline.md` and `PROMPT_USAGE.md` on the same stage model.

### Priority 3
Optionally refine the Make23 output wording once the stage model is fixed.

---

## Recommendation

Do **not** stop at the prompt files.
The next highest-value governance move is now to fix the pipeline-stage inconsistency, because it is the main remaining source of cross-stage ambiguity.
