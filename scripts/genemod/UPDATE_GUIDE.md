# Genemod Update Guide

This guide explains how to update the genemod system when the upstream repository
(https://github.com/Chinch-Bug/clangen-genemod) releases changes.

## Package Structure

All genemod code lives in `scripts/genemod/`:

| File | Upstream Source | Purpose |
|------|---------------|---------|
| `genotype.py` | `scripts/cat/genotype.py` | Genetic data model (60+ traits, generation, breeding) |
| `phenotype.py` | `scripts/cat/phenotype.py` | Converts genetics → visual traits |
| `breed_functions.py` | `scripts/cat/breed_functions.py` | 200+ breed validators & generators |
| `sprites.py` | N/A (local) | Genemod sprite asset loading |
| `__init__.py` | N/A (local) | Public interface / re-exports |

Backward-compatible shims exist at the old locations (`scripts/cat/genotype.py`, etc.)
so existing code continues working without import changes.

## How to Update

### Step 1: Get the new files from upstream

Download these files from the genemod repo:
- `scripts/cat/genotype.py` → copy to `scripts/genemod/genotype.py`
- `scripts/cat/phenotype.py` → copy to `scripts/genemod/phenotype.py`
- `scripts/cat/breed_functions.py` → copy to `scripts/genemod/breed_functions.py`

### Step 2: Fix internal imports

After copying, update these import lines in the new files:

**In `scripts/genemod/genotype.py`**, change:
```python
from scripts.cat.breed_functions import breed_functions
```
to:
```python
from scripts.genemod.breed_functions import breed_functions
```

**In `scripts/genemod/phenotype.py`**, change:
```python
from scripts.cat.breed_functions import find_my_breed
```
to:
```python
from scripts.genemod.breed_functions import find_my_breed
```

The `from .genotype import *` line in phenotype.py should work as-is (it's a relative import).

### Step 3: Update sprite assets

If the upstream added new sprite directories under `sprites/genemod/`:
1. Copy the new sprite files to `sprites/genemod/`
2. Update `scripts/genemod/sprites.py` to load the new sprite sheets/groups

### Step 4: Check for new API surface

If the upstream added new public classes, functions, or attributes that the rest of
the codebase needs, update `scripts/genemod/__init__.py` to export them.

### Step 5: Check integration points

These files in the main codebase consume genemod data. If the upstream changed
attribute names or method signatures, these may need updates:

| File | What it uses |
|------|-------------|
| `scripts/cat/cats.py` | `Genotype()`, `Phenotype()`, `.sexgene`, `.manx`, `.fold`, `.munch`, `.pax3`, `.chimerageno`, `GenerateWhite()` |
| `scripts/cat/pelts.py` | `Genotype`, `Phenotype`, `generate_new_pelt()` |
| `scripts/utility.py` | `Genotype()`, `Phenotype()`, `GenSprite()`, `.chimerageno` |
| `scripts/events_module/relationship/pregnancy_events.py` | `Genotype()`, `.sexgene` |
| `scripts/screens/MakeClanScreen.py` | `Genotype()`, `Phenotype()` |
| `scripts/screens/ProfileScreen.py` | `Phenotype()`, `.chimerageno` |
| `scripts/screens/ChooseMateScreen.py` | `.genotype.sexgene` via `xor()` |
| `scripts/events.py` | Various `.genotype.*` attributes |
| `scripts/events_module/generate_events.py` | `.genotype.sexgene`, `.phenotype.bobtailnr` |

### Step 6: Test

Run the game and verify:
- Cat generation works (new cats have valid genetics)
- Breeding produces kits with inherited traits
- Cat sprites render correctly
- Save/load preserves genetic data
- Breed detection works

## Key Genemod APIs (for reference)

```python
# Creating a cat's genetics
genotype = Genotype(game.config['genetics_config'], game.settings["ban problem genes"])
genotype.Generator()                   # random cat
genotype.KitGenerator(parent1, parent2) # breeding

# Converting to visual traits
phenotype = Phenotype(genotype)
phenotype.PhenotypeOutput(gender)

# Serialization
data = genotype.toJSON()
genotype.fromJSON(data)

# Breed detection
from scripts.genemod import find_my_breed
breed = find_my_breed(genotype, phenotype, config)

# Key attributes accessed by the rest of the codebase
genotype.sexgene        # ["o", "Y"] or ["O", "o"] etc.
genotype.manx           # [allele1, allele2] - tail gene
genotype.fold           # [allele1, allele2] - ear fold
genotype.munch          # [allele1, allele2] - short legs
genotype.pax3           # deafness/eye development
genotype.chimerageno    # secondary Genotype or None
genotype.white          # white spotting
genotype.white_pattern  # list of pattern names
genotype.chimera        # bool
```
