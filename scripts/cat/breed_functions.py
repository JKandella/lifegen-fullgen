"""
Backward-compatibility shim.
Actual implementation lives in scripts/genemod/breed_functions.py

All code in this file is re-exported from the genemod package.
Do not add new code here - modify scripts/genemod/breed_functions.py instead.
"""
from scripts.genemod.breed_functions import *  # noqa: F401,F403
from scripts.genemod.breed_functions import breed_functions, find_my_breed  # noqa: F401
