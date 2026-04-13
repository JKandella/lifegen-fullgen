"""
Genemod sprite loading.

This module extracts all genemod-specific sprite loading from scripts/cat/sprites.py
into a single function for easy updating. When the genemod upstream updates sprite
assets or adds new sprite groups, only this file needs updating.

The function takes a Sprites instance and calls its spritesheet() and make_group()
methods to register all genemod sprite assets.
"""
import os


def load_genemod_sprites(sprite_loader):
    """Load all genemod sprite assets into the given Sprites instance.

    Args:
        sprite_loader: A Sprites instance with spritesheet() and make_group() methods.
    """

    # --- Sprite sheets from genemod directories ---

    for x in os.listdir("sprites/genemod/borders"):
        sprite_loader.spritesheet("sprites/genemod/borders/"+x, 'genemod/'+x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/Base Colours"):
        sprite_loader.spritesheet("sprites/genemod/Base Colours/"+x, 'base/'+x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/points"):
        sprite_loader.spritesheet("sprites/genemod/points/"+x, x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/New Tabbies"):
        sprite_loader.spritesheet("sprites/genemod/New Tabbies/"+x, 'Tabby/'+x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/extra"):
        sprite_loader.spritesheet("sprites/genemod/extra/"+x, 'Other/'+x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/effects"):
        sprite_loader.spritesheet("sprites/genemod/effects/"+x, 'Other/'+x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/somatic"):
        sprite_loader.spritesheet("sprites/genemod/somatic/"+x, 'Somatic/'+x.replace('.png', ""))
        sprite_loader.make_group('Somatic/'+x.replace('.png', ""), (0, 0), "Somatic/"+x.replace('.png', ""))
    
    for x in os.listdir("sprites/genemod/white"):
        sprite_loader.spritesheet("sprites/genemod/white/"+x, 'White/'+x.replace('.png', ""))
        sprite_loader.make_group('White/'+x.replace('.png', ""), (0, 0), x.replace('.png', ""))
    for x in os.listdir("sprites/genemod/break white"):
        sprite_loader.spritesheet("sprites/genemod/break white/"+x, 'Break/'+x.replace('.png', ""))
        sprite_loader.make_group('Break/'+x.replace('.png', ""), (0, 0), 'break/'+x.replace('.png', ""))

    # --- Border and line art groups ---

    sprite_loader.make_group('genemod/normal border', (0, 0), 'normbord')
    sprite_loader.make_group('genemod/foldborder', (0, 0), 'foldbord')
    sprite_loader.make_group('genemod/curlborder', (0, 0), 'curlbord')
    sprite_loader.make_group('genemod/foldlineart', (0, 0), 'foldlines')
    sprite_loader.make_group('genemod/fold_curllineart', (0, 0), 'fold_curllines')
    sprite_loader.make_group('genemod/curllineart', (0, 0), 'curllines')
    sprite_loader.make_group('genemod/foldlineartdf', (0, 0), 'foldlineartdf')
    sprite_loader.make_group('genemod/fold_curllineartdf', (0, 0), 'fold_curllineartdf')
    sprite_loader.make_group('genemod/curllineartdf', (0, 0), 'curllineartdf')
    sprite_loader.make_group('genemod/foldlineartdead', (0, 0), 'foldlineartdead')
    sprite_loader.make_group('genemod/fold_curllineartdead', (0, 0), 'fold_curllineartdead')
    sprite_loader.make_group('genemod/curllineartdead', (0, 0), 'curllineartdead')

    sprite_loader.make_group('genemod/isolateears', (0, 0), 'isolateears')
    sprite_loader.make_group('genemod/noears', (0, 0), 'noears')
    
    sprite_loader.make_group('genemod/rexlines', (0, 0), 'rexlineart')
    sprite_loader.make_group('genemod/rexlinesdead', (0, 0), 'rexlineartdead')
    sprite_loader.make_group('genemod/rexlinesdf', (0, 0), 'rexlineartdf')
    sprite_loader.make_group('genemod/rexborder', (0, 0), 'rexbord')

    for a, x in enumerate(range(1, 6)):
        sprite_loader.make_group('genemod/bobtails', (a, 0), f'bobtail{x}')

    # --- Base colours ---

    sprite_loader.make_group('base/bases', (0, 0), 'basecolours', sprites_x=6, sprites_y=4)
    sprite_loader.make_group('base/lightbases', (0, 0), 'lightbasecolours', sprites_x=4, sprites_y=1)

    # --- Tabby bases ---

    for x in ["black", "blue", "dove", "platinum",
              "chocolate", "lilac", "champagne", "lavender",
              "cinnamon", "fawn", "buff", "beige",
              "red", "cream", "honey", "ivory"]:
        for a, i in enumerate(['rufousedlow', 'rufousedmedium', 'rufousedhigh', 'rufousedshaded', 'rufousedchinchilla']):
            sprite_loader.make_group('Tabby/'+x, (a, 0), f'{x}{i}', sprites_x=1, sprites_y=1)
        for a, i in enumerate(['mediumlow', 'mediummedium', 'mediumhigh', 'mediumshaded', 'mediumchinchilla']):
            sprite_loader.make_group('Tabby/'+x, (a, 1), f'{x}{i}', sprites_x=1, sprites_y=1)
        for a, i in enumerate(['lowlow', 'lowmedium', 'lowhigh', 'lowshaded', 'lowchinchilla']):
            sprite_loader.make_group('Tabby/'+x, (a, 2), f'{x}{i}', sprites_x=1, sprites_y=1)
        for a, i in enumerate(['silverlow', 'silvermedium', 'silverhigh', 'silvershaded', 'silverchinchilla']):
            sprite_loader.make_group('Tabby/'+x, (a, 3), f'{x}{i}', sprites_x=1, sprites_y=1)
    for a, x in enumerate(['low', 'medium', 'high', 'shaded', 'chinchilla']):
        sprite_loader.make_group('Tabby/shading', (a, 0), f'{x}shading')
    sprite_loader.make_group('Tabby/unders', (0, 0), f'Tabby_unders')

    # --- Tabby patterns ---

    for a, i in enumerate(['mackerel', 'brokenmack', 'spotted', 'classic', 'fullbar']):
        sprite_loader.make_group('Other/tabbypatterns', (a, 0), f'{i}')
    for a, i in enumerate(['braided', 'brokenbraid', 'rosetted', 'marbled', 'redbar']):
        sprite_loader.make_group('Other/tabbypatterns', (a, 1), f'{i}')
    for a, i in enumerate(['pinstripe', 'brokenpins', 'servaline', 'fullbarc', 'agouti']):
        sprite_loader.make_group('Other/tabbypatterns', (a, 2), f'{i}')
    for a, i in enumerate(['pinsbraided', 'brokenpinsbraid', 'leopard', 'redbarc', 'charcoal']):
        sprite_loader.make_group('Other/tabbypatterns', (a, 3), f'{i}')
    
    # --- Point markings ---

    sprite_loader.make_group('points_spring', (0, 0), 'pointsm')
    sprite_loader.make_group('points_summer', (0, 0), 'pointsl')
    sprite_loader.make_group('points_winter', (0, 0), 'pointsd')
    sprite_loader.make_group('mocha_spring', (0, 0), 'mocham')
    sprite_loader.make_group('mocha_summer', (0, 0), 'mochal')
    sprite_loader.make_group('mocha_winter', (0, 0), 'mochad')

    # --- Karpati ---

    for a, x in enumerate(['hetkarpatiwinter', 'hetkarpatispring', 'hetkarpatisummer']):
        sprite_loader.make_group('Other/karpati', (a, 0), x)
    for a, x in enumerate(['homokarpatiwinter', 'homokarpatispring', 'homokarpatisummer']):
        sprite_loader.make_group('Other/karpati', (a, 1), x)

    # --- Effects ---

    sprite_loader.make_group('Other/bimetal', (0, 0), 'bimetal')
    sprite_loader.make_group('Other/ghosting', (0, 0), 'ghost')
    sprite_loader.make_group('Other/tabbyghost', (0, 0), 'tabbyghost')
    sprite_loader.make_group('Other/grizzle', (0, 0), 'grizzle')
    sprite_loader.make_group('Other/smoke', (0, 0), 'smoke')
    sprite_loader.make_group('Other/bleach', (0, 0), 'bleach')
    sprite_loader.make_group('Other/lykoi', (0, 0), 'lykoi')
    sprite_loader.make_group('Other/hairless', (0, 0), 'hairless')
    sprite_loader.make_group('Other/donskoy', (0, 0), 'donskoy')
    sprite_loader.make_group('Other/furpoint', (0, 0), 'furpoint')
    sprite_loader.make_group('Other/caramel', (0, 0), 'caramel', 1, 1)
    sprite_loader.make_group('Other/satin', (0, 0), 'satin', 1, 1)
    sprite_loader.make_group('Other/salmiak', (0, 0), 'salmiak')

    # --- Extra (ears, noses, paw pads) ---

    sprite_loader.make_group('Other/ears', (0, 0), 'ears')
    sprite_loader.make_group('Other/noses', (0, 0), 'nose')
    sprite_loader.make_group('Other/nose_colours', (0, 0), 'nosecolours', sprites_y=5)
    sprite_loader.make_group('Other/paw_pads', (0, 0), 'pads')

    # --- Eyes ---

    for i, x in enumerate(['left', 'right', 'sectoral1', 'sectoral2', 'sectoral3', 'sectoral4', 'sectoral5', 'sectoral6']):
        sprite_loader.make_group('Other/eyebase', (i, 0), x, sprites_y=6)
    
    for b, x in enumerate(['P11', 'P10', 'P9', 'P8', 'P7', 'P6', 'P5', 'P4', 'P3', 'P2', 'P1', 'blue', 'albino']):
        for a, y in enumerate(range(1, 12)):
            sprite_loader.make_group('Other/eyes_full', (a, b), f'R{y} ; {x}/', sprites_y=6)
    
    sprite_loader.make_group('Other/red_pupils', (0, 0), 'redpupils')
