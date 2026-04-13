"""
Backward-compatibility shim.
Actual implementation lives in scripts/genemod/genotype.py

All code in this file is re-exported from the genemod package.
Do not add new code here - modify scripts/genemod/genotype.py instead.
"""
from scripts.genemod.genotype import *  # noqa: F401,F403
from scripts.genemod.genotype import Genotype  # noqa: F401 - explicit re-export
