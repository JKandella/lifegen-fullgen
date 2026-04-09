# Rewrite Plan

## Current State

This repository is not a clean fork of one mod with a second mod layered on top. It is a tightly coupled blend of LifeGen and GeneMod concepts inside the same runtime objects, save model, event pipeline, and UI flow.

## Upstream Findings

There are two different meanings of upstream here.

Immediate git upstream for this clone:

- local `origin` points to `JKandella/lifegen-fullgen`
- local `upstream` points to `ManiiaKop/lifegen-fullgen`
- current `development` is `12` commits ahead of `upstream/development` and `0` behind

Architectural upstreams for the code:

- The current repository shares a recent merge-base with `sedgestripe/clangen` at commit `12ab5c59`.
- That commit resolves to LifeGen tag `v0.7.5.4` and is dated `2025-04-01`.
- The current repository does **not** descend from current `LifeGen-dev`, but it clearly forked from a recent LifeGen release line and then diverged.
- The current repository also shares history with `Chinch-Bug/clangen-genemod`, but the merge-base is older: commit `639a1909`, dated `2024-12-12`.
- That indicates GeneMod is not the primary branch ancestry here; it is effectively a feature/code import layered onto a LifeGen-derived base.

Practical conclusion:

- Treat this project as a **LifeGen-derived fork with GeneMod integrations**, not as two equal upstream parents.
- For rewrite purposes, LifeGen is the more defensible starting lineage.
- GeneMod should be reintroduced as an isolated feature module, not used as the structural template for the rewritten runtime.

Observed characteristics:

- Player-cat logic is embedded in core simulation objects through `game.clan.your_cat` rather than isolated behind a mode or feature boundary.
- Genetics is embedded directly in `Cat` construction, persistence, pregnancy logic, sprite generation, and condition handling.
- The event system is a large monolith with LifeGen-specific behavior mixed into general clan simulation.
- Packaging and metadata still contain naming drift (`LifeGen`, `Genemod`, `ClanGen`) which is a maintenance smell and a release risk.
- Some core files are already beyond the size where safe feature work is cheap.

Hotspots by size:

- `scripts/cat/cats.py`: 4530 lines
- `scripts/events.py`: 4361 lines
- `scripts/clan.py`: 1910 lines
- `scripts/events_module/relationship/pregnancy_events.py`: 1551 lines
- `scripts/game_structure/load_cat.py`: 625 lines

## Rewrite Goal

The rewrite should not be a literal line-by-line port of this branch. The goal should be:

1. Choose a single upstream baseline.
2. Re-introduce LifeGen and GeneMod features behind explicit module boundaries.
3. Stabilize save compatibility with an adapter layer instead of spreading legacy conditionals across runtime code.
4. Make future upstream sync possible without re-merging giant files by hand.

## Recommended Direction

Use a recent ClanGen-compatible baseline as the core runtime, then port features in slices.

More specifically: prefer a modern LifeGen-compatible baseline over this repository's current branch shape.

Do not use this repository as the architecture template.

Reasoning:

- The current code mixes domain concerns in shared objects (`Cat`, `Clan`, `Events`).
- The player-focused LifeGen mode and the genetics-heavy GeneMod systems both override fundamental behavior.
- Large files and duplicated imports indicate the code has accumulated merge debt instead of clear boundaries.

## Target Architecture

Aim for these boundaries:

### Core Domain

- `Cat`, `Clan`, `Relationship`, `Event`, `PatrolOutcome`
- Core save model and migration layer
- Base simulation rules that work without any mod-specific features enabled

### Feature Modules

- `features/lifegen/`
  - player-cat state
  - dialogue and player choice systems
  - lead den, talk, date, murder, shun/forgive flows
- `features/genemod/`
  - genotype/phenotype model
  - breeding and inheritance rules
  - appearance generation and genetics-specific condition rules

### Adapters

- `adapters/save_compat/`
  - load old save fields
  - map old keys into the new internal model
- `adapters/content/`
  - event json loaders
  - patrol content loaders
  - pronoun/dialogue content loaders

### UI Layer

- screens should call feature services, not mutate core state directly
- window classes should not contain game-rule logic when it can live in services

## Migration Strategy

### Phase 1: Freeze the Legacy Shape

- Do not keep expanding giant files.
- Add architecture notes and module ownership rules.
- Identify legacy save fields that must remain loadable.
- Add a smoke-test baseline for save load, moon skip, pregnancy, and player-cat progression.

### Phase 2: Extract State Boundaries

- Introduce dedicated state containers for player mode and genetics.
- Replace direct reads of `game.clan.your_cat` in shared systems with a player context service.
- Move genotype/phenotype creation out of `Cat.__init__` behind a genetics service or factory.

### Phase 3: Split High-Risk Services

- Break `scripts/events.py` into event orchestration plus focused services.
- Break pregnancy and inheritance flows into isolated domain services.
- Move save migration rules out of runtime constructors.

### Phase 4: Port Screens to Service Calls

- Screens become thin controllers over feature and core services.
- Reduce direct mutation of `game`, `clan`, and `cat` objects from UI handlers.

### Phase 5: Delete Legacy Glue

- Remove compatibility branches that were only needed during migration.
- Normalize naming across packaging and release files.
- Re-run a full save migration pass and content validation.

## First Implementation Slice

The safest first rewrite slice is not `events.py` as a whole. It is extracting the player-cat boundary.

Create a dedicated `PlayerContext` or `LifeGenState` service that owns:

- selected player cat id
- player-specific flags and counters
- helper methods currently spread across `Clan`, `Events`, `Patrol`, and window logic

Initial benefits:

- removes direct coupling to `game.clan.your_cat`
- creates a seam for testing player-mode behavior
- reduces the amount of shared simulation code that must know LifeGen exists

Suggested first targets for this extraction:

- `scripts/clan.py`
- `scripts/game_structure/windows.py`
- `scripts/events_module/patrol/patrol.py`
- `scripts/events_module/relationship/romantic_events.py`
- `scripts/events_module/relationship/pregnancy_events.py`

## Save Compatibility Rules

Treat save compatibility as a separate problem.

- Old save keys like `your_cat`, `genotype`, `phenotype`, `shunned`, and `forgiven` should be loaded by migration code.
- Runtime domain objects should receive normalized data, not legacy branches.
- Versioned migration functions are easier to test than scattered `if key in save` checks.

## Testing Baseline Needed Before Any Large Port

Before broad rewrites, add automated checks for:

- loading an existing clan save
- creating a new clan with player-cat mode enabled
- one moon progression
- pregnancy and kit generation
- pronoun replacement content
- patrol generation for player and non-player cases

Note: the current workspace virtual environment does not include `pytest`, so test execution is not ready until the environment is brought in line with the project config.

## Definition of Success

The rewrite is succeeding if:

- new features can be added without editing `Cat`, `Clan`, and `Events` at the same time
- player-mode code can be disabled without breaking core clan simulation
- genetics can be tested independently of screens and save loading
- upstream syncs require feature ports, not giant conflict resolution sessions

## Immediate Next Step

Implement the player context extraction first, then convert one narrow path end-to-end:

1. new clan creation
2. selecting the player cat
3. one player-driven moon progression
4. saving and loading that state

If that slice lands cleanly, use the same pattern for genetics state and inheritance services.