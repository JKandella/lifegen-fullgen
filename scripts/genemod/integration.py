"""
Genemod Integration Layer
=========================

Bridges genemod's genetics system with lifegen's pelt/sprite system.
This module maps genotype/phenotype data to lifegen's named pelt attributes
so the existing sprite rendering pipeline can display genetics-based cats.

This keeps genemod's genetics functionally important (breeding, conditions, sex)
while using lifegen's sprite system for rendering (as an approximation).
"""

from random import choice
from scripts.genemod.genotype import Genotype
from scripts.genemod.phenotype import Phenotype


# --------------------------------------------------------------------------- #
#                          Phenotype -> Pelt Mapping                           #
# --------------------------------------------------------------------------- #

# Maps genemod phenotype colour names to lifegen pelt colour names
COLOUR_MAP = {
    # eumelanin colours
    "black": "BLACK",
    "chocolate": "CHOCOLATE",
    "cinnamon": "LIGHTBROWN",
    "blue": "GREY",
    "lilac": "LILAC",
    "fawn": "PALEGINGER",
    "dove": "PALEGREY",
    "champagne": "LILAC",
    "buff": "LIGHTBROWN",
    "platinum": "SILVER",
    "lavender": "LILAC",
    "beige": "PALEGINGER",
    "sable": "DARKBROWN",
    "seal": "DARKBROWN",

    # phaeomelanin colours
    "red": "DARKGINGER",
    "cream": "CREAM",
    "honey": "GOLDEN",
    "ivory": "PALEGINGER",
    "flame": "GINGER",

    # special
    "white": "WHITE",
    "albino": "WHITE",
}

# Maps genemod phenotype tabby patterns to lifegen pelt pattern names
PATTERN_MAP = {
    "mackerel": "Mackerel",
    "broken mackerel": "Mackerel",
    "blotched": "Classic",
    "spotted": "Speckled",
    "ticked": "Ticked",
    "agouti": "Agouti",
    "chinchilla": "Agouti",
    "shaded": "Agouti",
    "rosetted": "Rosette",
    "braided": "Bengal",
    "broken braided": "Bengal",
    "marbled": "Marbled",
    "sokoke": "Sokoke",
    "servaline": "Speckled",
    "ghost-patterned": "Classic",
    "ghost marble": "Marbled",
    "pinstripe": "Mackerel",
    "broken pinstripe": "Mackerel",
    "servaline-rosetted": "Rosette",
    "pinstripe-braided": "Bengal",
    "broken pinstripe-braided": "Bengal",
    "brokenpins": "Mackerel",
    "brokenmack": "Mackerel",
    "brokenbraid": "Bengal",
    "brokenpinsbraid": "Bengal",
    "leopard": "Rosette",
    "pinsbraided": "Bengal",
}

# Maps genemod eye names to lifegen eye colour names
EYE_MAP = {
    "yellow": "YELLOW",
    "golden": "GOLD",
    "amber": "AMBER",
    "orange": "ORANGE",
    "copper": "COPPER",
    "bronze": "BRONZE",
    "hazel": "HAZEL",
    "green": "GREEN",
    "emerald": "EMERALD",
    "pale green": "PALEGREEN",
    "sage": "SAGE",
    "cyan": "CYAN",
    "blue": "BLUE",
    "dark blue": "DARKBLUE",
    "pale blue": "PALEBLUE",
    "heather blue": "HEATHERBLUE",
    "cobalt": "COBALT",
    "grey": "GREY",
    "sunlit ice": "SUNLITICE",
    "grey-green": "SAGE",
    "green-yellow": "GREENYELLOW",
    "pale yellow": "PALEYELLOW",
    "silver": "SILVER",
    "pink": "PALEBLUE",
    "albino": "PALEBLUE",
}

# Maps genemod white grade + alleles to lifegen white patch choices
WHITE_PATCHES_LITTLE = [
    "LITTLE", "EXTRA", "PAWS", "TOES", "BIB", "VEE", "TAILTIP",
    "BLAZE", "BELLY", "TOESTAIL", "BROKENBLAZE", "SCOURGE",
    "BUZZARDFANG", "RAVENPAW", "LILTWO", "LUNA",
]
WHITE_PATCHES_MID = [
    "TUXEDO", "FANCY", "UNDERS", "DAMIEN", "SKUNK", "TOPCOVER",
    "DIVA", "SQUEAKS", "STAR", "BEARD", "MITAINE", "SAVANNAH",
    "FADESPOTS", "DAPPLEPAW",
]
WHITE_PATCHES_HIGH = [
    "ANY", "ANYTWO", "BROKEN", "FRECKLES", "HALFFACE", "PANTSTWO",
    "GOATEE", "PIEBALD", "CURVED", "OWL", "SHIBAINU", "RINGTAIL",
    "HALFWHITE", "APPALOOSA", "PANTS", "REVERSEPANTS", "MASKMANTLE",
    "FAROFA", "PRINCE", "MISTER", "MAO", "GLASS", "PAINTED",
]
WHITE_PATCHES_MOSTLY = [
    "VAN", "ONEEAR", "LIGHTSONG", "TAIL", "PETAL", "BLACKSTAR",
    "PEBBLESHINE", "CAPSADDLE", "APRON", "CHESTSPECK", "HEART",
    "HEARTTWO", "MOORISH",
]

POINT_PATCHES = {
    "point": "COLOURPOINT",
    "mink": "MINKPOINT",
    "sepia": "SEPIAPOINT",
    "siamocha": "COLOURPOINT",
    "burmocha": "SEPIAPOINT",
    "mocha": "SEPIAPOINT",
}


def map_eye_colour(eye_name):
    """Map a genemod eye colour name to a lifegen eye colour sprite name."""
    if not eye_name:
        return "YELLOW"
    eye_lower = eye_name.lower().strip()
    return EYE_MAP.get(eye_lower, "YELLOW")


def map_pelt_colour(phenotype):
    """Map genemod phenotype colour to lifegen pelt colour name."""
    if not phenotype or not phenotype.colour:
        return "BLACK"

    colour = phenotype.colour.strip().lower()

    # Remove modifiers
    for modifier in ["caramel", "apricot", "light ", "non", "agouti "]:
        colour = colour.replace(modifier, "").strip()

    return COLOUR_MAP.get(colour, "BLACK")


def map_pelt_pattern(genotype, phenotype):
    """Map genemod phenotype pattern to lifegen pelt pattern name."""
    if not phenotype:
        return "SingleColour"

    # Solid white overrides everything
    if genotype and (genotype.white[0] == "W" or genotype.pointgene[0] == "c"):
        return "SingleColour"

    # Check for tortie/calico
    is_tortie = phenotype.tortie.strip() != "" if phenotype.tortie else False

    # Smoke check
    if phenotype.silvergold and "smoke" in phenotype.silvergold.lower():
        if not phenotype.tabby or phenotype.tabby.strip() == "":
            if is_tortie:
                return "Tortie"
            return "Smoke"

    # Tabby patterns
    tabby = phenotype.tabby.strip().lower() if phenotype.tabby else ""
    # Strip suffixes like " tabby ", " lynx "
    tabby = tabby.replace(" tabby ", "").replace(" lynx ", "").strip()

    if is_tortie:
        if tabby:
            return "Calico" if ("calico" in phenotype.tortie.lower() or "caliby" in phenotype.tortie.lower()) else "Tortie"
        return "Calico" if "calico" in phenotype.tortie.lower() else "Tortie"

    if tabby:
        return PATTERN_MAP.get(tabby, "Tabby")

    return "SingleColour"


def map_white_patches(genotype, phenotype):
    """Map genemod white patterns to lifegen white patch name."""
    if not genotype:
        return None, None, None

    # Solid white - no patches needed (colour is white)
    if genotype.white[0] == "W" or genotype.pointgene[0] == "c":
        return None, None, None

    white_patches = None
    points = None
    vitiligo = None

    # Vitiligo
    if genotype.vitiligo:
        vitiligo = "VITILIGO"

    # Karpati
    if genotype.karp[0] == "K":
        vitiligo = "KARPATI"

    # Point markings (colourpoint, mink, sepia)
    point_name = phenotype.point.strip().lower() if phenotype.point else ""
    if point_name and point_name in POINT_PATCHES:
        points = POINT_PATCHES[point_name]

    # White spotting
    if genotype.white[1] in ["ws", "wt"] or ("NoDBE" not in genotype.pax3 and "DBEalt" in genotype.pax3):
        # High white
        if genotype.whitegrade > 3:
            white_patches = choice(WHITE_PATCHES_MOSTLY)
        else:
            white_patches = choice(WHITE_PATCHES_HIGH)
    elif genotype.white[0] in ["ws", "wt"]:
        if genotype.whitegrade > 3:
            white_patches = choice(WHITE_PATCHES_HIGH)
        elif genotype.whitegrade > 1:
            white_patches = choice(WHITE_PATCHES_MID)
        else:
            white_patches = choice(WHITE_PATCHES_LITTLE)
    elif genotype.white[0] == "wg":
        # Birman gloving - use little white
        white_patches = choice(WHITE_PATCHES_LITTLE)
    elif genotype.white[0] == "wsal":
        # Salmiak
        white_patches = choice(WHITE_PATCHES_MID)

    return white_patches, points, vitiligo


def map_tortie_patches(genotype, phenotype):
    """Map genemod tortie pattern to lifegen tortie attributes."""
    if not phenotype or not phenotype.tortie or phenotype.tortie.strip() == "":
        return None, None, None, None

    # tortie_marking is the pattern mask (from genotype.tortiepattern or genotype.white_pattern)
    tortie_marking = None
    if hasattr(genotype, "tortiepattern") and genotype.tortiepattern:
        tortie_marking = genotype.tortiepattern
    elif hasattr(genotype, "white_pattern") and genotype.white_pattern:
        # white_pattern is a list
        if isinstance(genotype.white_pattern, list) and genotype.white_pattern:
            tortie_marking = genotype.white_pattern[0]

    if tortie_marking == "CRYPTIC":
        return None, None, None, None

    # Get the red/ginger colour for tortie patches
    # Tortie base is the eumelanin colour, patches are the phaeomelanin colour
    genotype_copy = genotype
    if genotype_copy.dilute[0] == "d":
        tortie_colour = "CREAM"
    else:
        tortie_colour = "GINGER"

    # Base pattern for the tortie patches
    tabby = phenotype.tabby.strip().lower() if phenotype.tabby else ""
    tabby = tabby.replace(" tabby ", "").replace(" lynx ", "").strip()
    if tabby:
        tortie_base = PATTERN_MAP.get(tabby, "single")
        # lifegen uses lowercase pattern names for tortie_base
        tortie_base = tortie_base[0].lower() + tortie_base[1:] if tortie_base else "single"
    else:
        tortie_base = "single"

    # Pattern name ("SingleColour" -> "Single" for the base coat)
    tortie_pattern = map_pelt_pattern(genotype, phenotype)
    if tortie_pattern in ("Tortie", "Calico"):
        # The tortie_pattern field in lifegen is the pattern of the patches
        tortie_pattern = "SingleColour" if not tabby else PATTERN_MAP.get(tabby, "Tabby")

    return tortie_marking, tortie_base, tortie_colour, tortie_pattern


def map_skin_colour(genotype):
    """Map genotype to skin/nose colour."""
    if not genotype:
        return "BLACK"

    if genotype.white[0] == "W" or genotype.pointgene[0] == "c":
        return "PINK"

    if genotype.eumelanin[0] == "B":
        if genotype.dilute[0] == "d":
            return "BLUE"
        return "BLACK"
    elif genotype.eumelanin[0] == "b":
        if genotype.dilute[0] == "d":
            return "PINK"
        return "CHOCOLATE"
    else:
        return "PINK"


def map_pelt_length(phenotype):
    """Map genemod phenotype length to lifegen pelt length."""
    if not phenotype or not phenotype.length:
        return "short"
    length = phenotype.length.lower()
    if "longhaired" in length:
        return "long"
    elif "mediumhaired" in length or "medium" in length:
        return "medium"
    elif "hairless" in length or "fur-pointed" in length:
        return "short"
    return "short"


# --------------------------------------------------------------------------- #
#                        Genotype <-> Cat Lifecycle                            #
# --------------------------------------------------------------------------- #

def create_genotype(genetics_config, ban_genes=True):
    """Create a new random genotype with default genetics."""
    genotype = Genotype(genetics_config, ban_genes)
    return genotype


def generate_cat_genetics(genetics_config, gender, ban_genes=True):
    """Generate a new cat's genotype + phenotype from scratch."""
    genotype = Genotype(genetics_config, ban_genes)
    special = None
    if gender == "male":
        special = "masc"
    elif gender == "female":
        special = "fem"
    genotype.Generator(special)
    phenotype = Phenotype(genotype)
    phenotype.PhenotypeOutput(gender)
    return genotype, phenotype


def generate_kit_genetics(genetics_config, parent1_genotype, parent2_genotype=None, ban_genes=True):
    """Generate genetics for a kit from parent genotypes."""
    genotype = Genotype(genetics_config, ban_genes)
    genotype.KitGenerator(parent1_genotype, parent2_genotype)
    phenotype = Phenotype(genotype)
    phenotype.PhenotypeOutput()
    return genotype, phenotype


def load_genotype_from_json(genetics_config, json_data, ban_genes=True):
    """Load a genotype from saved JSON data."""
    genotype = Genotype(genetics_config, ban_genes)
    genotype.fromJSON(json_data)
    phenotype = Phenotype(genotype)
    phenotype.PhenotypeOutput()
    return genotype, phenotype


def apply_genetics_to_pelt(pelt, genotype, phenotype):
    """Apply genotype/phenotype data to an existing lifegen Pelt object.

    This maps genetics to the pelt's named attributes so lifegen's
    sprite system can render the cat.
    """
    if not genotype or not phenotype:
        return

    # Colour
    pelt.colour = map_pelt_colour(phenotype)

    # Pattern
    pelt.name = map_pelt_pattern(genotype, phenotype)

    # Length
    pelt.length = map_pelt_length(phenotype)

    # White patches
    white_patches, points, vitiligo = map_white_patches(genotype, phenotype)
    pelt.white_patches = white_patches
    pelt.points = points
    pelt.vitiligo = vitiligo

    # Eyes
    pelt.eye_colour = map_eye_colour(genotype.lefteye)
    if genotype.lefteye != genotype.righteye:
        pelt.eye_colour2 = map_eye_colour(genotype.righteye)
    else:
        pelt.eye_colour2 = None
    if genotype.extraeye:
        # Sectoral heterochromia - approximate with heterochromia
        if not pelt.eye_colour2:
            pelt.eye_colour2 = map_eye_colour(genotype.righteye)

    # Skin
    pelt.skin = map_skin_colour(genotype)

    # Tortie
    if phenotype.tortie and phenotype.tortie.strip():
        tortie_marking, tortie_base, tortie_colour, tortie_pattern = map_tortie_patches(genotype, phenotype)
        pelt.tortie_marking = tortie_marking
        pelt.tortie_base = tortie_base
        pelt.tortie_colour = tortie_colour
        pelt.tortie_pattern = tortie_pattern
    else:
        pelt.tortie_marking = None
        pelt.tortie_base = None
        pelt.tortie_colour = None
        pelt.tortie_pattern = None

    pelt.rebuild_sprite = True


def get_gender_from_genotype(genotype):
    """Determine gender from genotype's sex chromosomes."""
    if not genotype:
        return None
    if "Y" in genotype.sexgene:
        return "male"
    return "female"


def check_viability(genotype):
    """Check if a cat with this genotype would be stillborn.

    Returns True if the cat is viable (alive), False if stillborn.
    """
    if not genotype:
        return True

    # Lethal homozygous conditions
    if genotype.munch[1] == "Mk":
        return False
    if genotype.fold[1] == "Fd":
        return False
    if genotype.manx == ["M", "M"]:
        return False
    if "NoDBE" not in genotype.pax3 and "DBEalt" not in genotype.pax3:
        return False

    return True


def get_genetic_conditions(genotype, phenotype):
    """Return a list of genetic conditions this cat may have.

    Returns list of condition name strings compatible with lifegen's
    condition system.
    """
    conditions = []
    if not genotype:
        return conditions

    # Deafness from dominant white
    if genotype.white[0] == "W":
        if genotype.deaf:
            conditions.append("deaf")

    # Manx syndrome (spinal issues from Manx gene)
    if genotype.manx[0] == "M":
        if genotype.manxtype in ("rumpy", "riser"):
            # Higher chance of manx syndrome
            conditions.append("manx_syndrome_risk")

    # Folded-ear joint issues
    if genotype.fold[0] == "Fd":
        conditions.append("joint pain")

    # Munchkin joint issues
    if genotype.munch[0] == "Mk":
        conditions.append("joint pain")

    # Hairless cats - skin issues
    if phenotype and phenotype.length == "hairless":
        conditions.append("hairless")

    # Lykoi - sparse fur
    if genotype.lykoi[0] == "ly":
        conditions.append("sparse_fur")

    return conditions
