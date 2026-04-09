"""
Compatibility shims so GeneMod's internal files can import stable names
that map onto LifeGen's runtime without modification.

When LifeGen restructures a setting or GeneMod renames a helper,
only this file needs to change.
"""
from __future__ import annotations


def get_clan_setting(key: str):
    """
    Drop-in replacement for GeneMod's clan_package.settings.get_clan_setting.
    Reads from game.clan.clan_settings which is LifeGen's equivalent store.
    Returns False if the clan or setting does not exist yet (e.g. during init).
    """
    try:
        from scripts.game_structure.game_essentials import game
        if game.clan and hasattr(game.clan, "clan_settings"):
            return game.clan.clan_settings.get(key, False)
        return False
    except Exception:
        return False
