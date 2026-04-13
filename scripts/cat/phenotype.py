"""
Backward-compatibility shim.
Actual implementation lives in scripts/genemod/phenotype.py

All code in this file is re-exported from the genemod package.
Do not add new code here - modify scripts/genemod/phenotype.py instead.
"""
from scripts.genemod.phenotype import *  # noqa: F401,F403
from scripts.genemod.phenotype import Phenotype  # noqa: F401 - explicit re-export
