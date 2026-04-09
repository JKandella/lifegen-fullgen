# Mod Abstraction Audit

Last updated: 2026-04-09
Branch: rewrite/base-v0.7.6.4
Goal: keep LifeGen core aligned with development while isolating GeneMod behavior behind stable interfaces.

## Scope

This document tracks remaining coupling points between core LifeGen code and GeneMod behavior.
Update this file whenever a coupling point is added, removed, or moved.

## Current Adapter Surface

- scripts/genemod/genetics_service.py
  - init_cat(...)
  - to_json(...)
  - from_json(...)
  - generate_kit_genotype(...)
  - generate_random_genotype(...)
  - compute_phenotype(...)

## Coupling Inventory (Needs Abstraction)

### 1) Core genotype implementation still in core path

- scripts/cat/genotype.py
  - Status: OPEN
  - Why it matters: this is GeneMod-owned behavior but still located in core namespace.
  - Target: move implementation ownership to scripts/genemod, keep scripts/cat/genotype.py as compatibility shim until full cutover.

### 2) Core phenotype inheritance from core genotype

- scripts/cat/phenotype.py
  - Status: OPEN
  - Why it matters: phenotype currently depends on Genotype class hierarchy directly.
  - Target: avoid direct class coupling where possible and rely on service/factory boundaries.

### 3) Cat module still imports adapter directly

- scripts/cat/cats.py
  - Status: PARTIAL (improved, still core-aware)
  - Current state: cat init/save path uses GeneticsService.
  - Target: keep only stable service calls from core; no direct schema assumptions outside service contracts.

### 4) Pregnancy path still has direct genotype field logic

- scripts/events_module/relationship/pregnancy_events.py
  - Status: PARTIAL (constructor path abstracted, field-level coupling remains)
  - Current state: random genotype creation now goes through GeneticsService.
  - Remaining coupling: many direct reads of genotype internals (sexgene, manx, fold, munch, pax3).
  - Target: move high-level pregnancy genetics decisions into service helpers so pregnancy_events does not depend on low-level genotype schema.

### 5) Genotype depends on genemod compatibility helper from core path

- scripts/cat/genotype.py -> scripts/genemod/compat.py
  - Status: OPEN
  - Why it matters: reverse dependency from core namespace to mod namespace.
  - Target: push setting lookups into service/config adapter layer.

### 6) Raw genetics config shape not normalized in a single adapter

- resources/game_config.json (genetics_config)
- scripts/genemod/genetics_service.py (reads genetics_config directly)
- scripts/cat/genotype.py (expects many specific keys)
  - Status: PARTIAL
  - Why it matters: schema drift causes fallback/default patches in Genotype.
  - Target: add one normalization step in service layer that guarantees complete, stable odds schema before Genotype sees it.

### 7) Rendering/pelt logic reads genotype internals directly

- scripts/cat/pelts.py
  - Status: OPEN
  - Why it matters: UI/render logic tightly coupled to gene storage layout.
  - Target: expose phenotype/render-facing traits from service/phenotype API and reduce direct genotype field access.

### 8) Event generation logic checks raw sexgene directly

- scripts/events_module/generate_events.py
  - Status: OPEN
  - Why it matters: event rules tied to internal genotype representation.
  - Target: replace raw sexgene checks with adapter-level helpers (for example, sex/role compatibility helpers).

## Migration Plan (Incremental)

### Slice A: Stabilize service boundaries

- Add helper methods in GeneticsService for frequent rule checks used outside genetics internals.
- Replace repeated raw genotype field checks in pregnancy/events with those helpers.
- Progress: pregnancy random-parent genotype construction now uses GeneticsService.generate_random_genotype(...); tests.test_relation_events and tests.test_romantic_events pass on this slice.

### Slice B: Introduce schema normalization

- Add one function that normalizes genetics_config into complete odds.
- Remove scattered fallback defaults once normalization is trusted by tests.

### Slice C: Move implementation ownership

- Create scripts/genemod genotype implementation module.
- Keep scripts/cat/genotype.py as shim/re-export during transition.
- Convert remaining direct imports to service/factory usage.

### Slice D: Reduce core field-level coupling

- Replace direct genotype field reads in pelts/events with stable accessor/helper API.

## Definition of Done

- Core LifeGen modules do not import GeneMod internals except approved adapter entry points.
- No core module relies on raw genotype schema details that are mod-specific.
- Genotype config normalization exists in one place.
- scripts/cat/genotype.py is either a compatibility shim or removed after full import migration.
- Targeted tests pass after each slice.

## Update Protocol

When making a new abstraction change, update this file in the same commit:

1. Move affected item status (OPEN/PARTIAL/DONE).
2. Add or remove exact file paths under Coupling Inventory.
3. Add a one-line note under the relevant migration slice.
4. Update Last updated date.

This keeps the architecture drift visible and prevents regressions during merge cycles.
