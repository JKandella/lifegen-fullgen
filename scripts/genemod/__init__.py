"""
Genemod - Realistic Cat Genetics System
========================================

This package contains the genemod (genetic modification) system, originally from:
https://github.com/Chinch-Bug/clangen-genemod

It provides realistic cat genetics including color inheritance, body modifications,
breed validation, and visual trait calculation.

Public API
----------
- Genotype(odds, ban_genes=True, spec=None) : Genetic data model
  - .Generator(special=None, kittypet=False) : Generate random genetics
  - .KitGenerator(par1, par2, par3, chimera, gender) : Breed cats
  - .fromJSON(data) / .toJSON()      : Serialization
  - .sexgene, .manx, .fold, .munch, .pax3 : Key trait access

- Phenotype(odds, ban_genes=True) : Visual trait calculator (inherits Genotype)
  - .PhenotypeOutput(pattern, gender, chimera) : Convert genotype to visual traits
  - .FurtypeFinder()                 : Determine fur texture description

- breed_functions : dict
  - ["generator"][breed_name]        : Breed-specific generation functions
  - ["checker"][breed_name]          : Breed validation functions

- find_my_breed(phenotype) : Determine breed from genetics

Integration Layer (scripts.genemod.integration)
------------------------------------------------
The integration module bridges genemod's genetics with lifegen's pelt/sprite
system. Callers should use these functions instead of Genotype/Phenotype directly:
  - generate_cat_genetics(config, gender, ban_genes)
  - generate_kit_genetics(config, par1_geno, par2_geno, ban_genes)
  - load_genotype_from_json(config, json_data, ban_genes)
  - apply_genetics_to_pelt(pelt, genotype, phenotype)

Updating from upstream genemod
------------------------------
See UPDATE_GUIDE.md in this directory.
"""

from scripts.genemod.genotype import Genotype
from scripts.genemod.phenotype import Phenotype
from scripts.genemod.breed_functions import breed_functions, find_my_breed

__all__ = [
    "Genotype",
    "Phenotype",
    "breed_functions",
    "find_my_breed",
    "integration",
]
