"""
GeneticsService - stable adapter between LifeGen and GeneMod.

All LifeGen code that needs genetics calls methods here.
When GeneMod updates its internal API, only this file changes.
When LifeGen updates its Cat/Pelt code, nothing here breaks.

Usage:
    from scripts.genemod.genetics_service import GeneticsService

    # On Cat init
    geno, pheno = GeneticsService.init_cat(
        genotype_json=genotype,
        parent1=parent1,
        parent2=parent2,
        extrapar=extrapar,
        kittypet=kittypet,
        gender=self.gender,
        status=status,
    )
    self.genotype = geno
    self.phenotype = pheno
"""
from __future__ import annotations

from random import randint
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.cat.genotype import Genotype
    from scripts.cat.phenotype import Phenotype


class GeneticsService:
    """
    Stable interface to the GeneMod genetics system.

    All methods are static. Cat instances are never held here.
    """

    # ------------------------------------------------------------------ #
    # Cat initialisation                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def init_cat(
        genotype_json=None,
        white_patterns=None,
        chim_white=None,
        parent1: Optional[str] = None,
        parent2: Optional[str] = None,
        extrapar=None,
        kittypet: bool = False,
        gender: Optional[str] = None,
        status: str = "newborn",
    ) -> tuple["Genotype", "Phenotype"]:
        """
        Create and return (genotype, phenotype) for a newly constructed Cat.

        Pass genotype_json when loading an existing cat from a save file.
        Pass parent1/parent2 IDs when spawning a kit from two parents.
        Pass kittypet=True or status='kittypet' for kittypet/outsider generation.
        """
        from scripts.cat.genotype import Genotype
        from scripts.cat.phenotype import Phenotype
        from scripts.game_structure.game_essentials import game

        odds = game.config.get("genetics_config", {})
        ban_genes = game.settings.get("ban problem genes", True)

        geno = Genotype(odds, ban_genes)

        if genotype_json:
            geno.fromJSON(genotype_json)
            if white_patterns is not None:
                geno.white_pattern = white_patterns
            if chim_white is not None:
                chimera_geno = getattr(geno, "chimerageno", None)
                if chimera_geno is not None:
                    setattr(chimera_geno, "white_pattern", chim_white)
        elif parent1 or parent2:
            geno = GeneticsService._generate_kit(geno, parent1, parent2, extrapar)
        elif kittypet or status == "kittypet":
            geno.AltGenerator(special=gender)
        else:
            geno.Generator(special=gender)

        GeneticsService._maybe_apply_intersex(geno, odds)

        pheno = GeneticsService._compute_phenotype(geno)
        return geno, pheno

    # ------------------------------------------------------------------ #
    # Save / load                                                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_json(genotype: "Genotype") -> dict:
        """Serialise a genotype to a JSON-safe dict for saving."""
        return genotype.toJSON()

    @staticmethod
    def from_json(data: dict) -> "Genotype":
        """Deserialise a genotype from a saved dict."""
        from scripts.cat.genotype import Genotype
        from scripts.game_structure.game_essentials import game

        odds = game.config.get("genetics_config", {})
        ban_genes = game.settings.get("ban problem genes", True)
        geno = Genotype(odds, ban_genes)
        geno.fromJSON(data)
        return geno

    # ------------------------------------------------------------------ #
    # Breeding                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_kit_genotype(
        parent1_genotype: "Genotype",
        parent2_genotype: Optional["Genotype"],
        extrapar=None,
    ) -> "Genotype":
        """Generate a kit genotype from one or two parent genotypes."""
        from scripts.cat.genotype import Genotype
        from scripts.game_structure.game_essentials import game

        odds = game.config.get("genetics_config", {})
        ban_genes = game.settings.get("ban problem genes", True)
        geno = Genotype(odds, ban_genes)
        geno.KitGenerator(parent1_genotype, parent2_genotype or extrapar)
        return geno

    @staticmethod
    def compute_phenotype(genotype: "Genotype") -> "Phenotype":
        """Compute the visible traits from a genotype."""
        return GeneticsService._compute_phenotype(genotype)

    # ------------------------------------------------------------------ #
    # Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _generate_kit(geno, parent1_id, parent2_id, extrapar):
        from scripts.cat.cats import Cat
        from scripts.cat.genotype import Genotype

        if not parent1_id:
            geno.KitGenerator(Cat.all_cats[parent2_id].genotype, extrapar)
        elif not parent2_id:
            geno.KitGenerator(Cat.all_cats[parent1_id].genotype, extrapar)
        else:
            try:
                geno.KitGenerator(
                    Cat.all_cats[parent1_id].genotype,
                    Cat.all_cats.get(parent2_id, extrapar),
                )
            except Exception as e:
                print(f"GeneticsService.KitGenerator: {e}")
                geno.Generator()
        return geno

    @staticmethod
    def _maybe_apply_intersex(geno, odds: dict):
        intersex_chance = odds.get("intersex", 100)
        if randint(1, intersex_chance) == 1:
            geno.gender = "intersex"
            if randint(1, 25) == 1 and "Y" in geno.sexgene:
                geno.gender = "molly"

    @staticmethod
    def _compute_phenotype(geno) -> "Phenotype":
        from scripts.cat.phenotype import Phenotype

        pheno = Phenotype(geno.odds, geno.ban_genes)
        pheno.__dict__.update(geno.__dict__)
        pheno.PhenotypeOutput(getattr(geno, "gender", getattr(geno, "sex", None)))
        if getattr(geno, "chimerageno", None):
            chim_pheno = Phenotype(geno.chimerageno.odds, geno.chimerageno.ban_genes)
            chim_pheno.__dict__.update(geno.chimerageno.__dict__)
            chim_pheno.PhenotypeOutput(
                getattr(geno.chimerageno, "gender", getattr(geno.chimerageno, "sex", None))
            )
            # Attach chimera phenotype to the main phenotype for callers that need it
            setattr(pheno, "chimerapheno", chim_pheno)
        return pheno
