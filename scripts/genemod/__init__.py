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
  - .Generator(special=None)         : Generate random genetics
  - .KitGenerator(parent1, parent2)  : Breed two cats
  - .fromJSON(data) / .toJSON()      : Serialization
  - .sexgene, .manx, .fold, .munch, .pax3 : Key trait access
  - .chimerageno                     : Secondary genotype for chimeras

- Phenotype(genotype) : Visual trait calculator
  - .PhenotypeOutput(gender)         : Convert genotype to visual traits
  - .FurtypeFinder()                 : Determine fur texture description

- breed_functions : dict
  - ["generator"][breed_name]        : Breed-specific generation functions
  - ["checker"][breed_name]          : Breed validation functions

- find_my_breed(genotype, phenotype, config) : Determine breed from genetics

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
