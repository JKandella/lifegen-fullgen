import os
import unittest

from scripts.cat_relations.enums import rel_type_tiers, RelType

from scripts.cat.enums import CatRank

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from scripts.cat.cats import Cat, Relationship
from scripts.cat.skills import SkillPath, Skill
from scripts.cat_relations.interaction import (
    SingleInteraction,
    cats_fulfill_single_interaction_constraints,
)


class RelationshipConstraints(unittest.TestCase):
    def test_siblings(self):
        # given
        parent = Cat()
        cat_from = Cat(parent1=parent.ID)
        cat_to = Cat(parent1=parent.ID)

        # then
        interaction = SingleInteraction("test")
        interaction.relationship_constraint = ["siblings"]
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(cat_from, cat_to, interaction)
        )

        interaction_neg = SingleInteraction("test")
        interaction_neg.relationship_constraint = ["-mates"]
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(cat_from, cat_to, interaction_neg)
        )

    def test_mates(self):
        # given
        cat_from = Cat()
        cat_to = Cat()
        cat_from.mate.append(cat_to.ID)
        cat_to.mate.append(cat_from.ID)

        # then
        interaction = SingleInteraction("test")
        interaction.relationship_constraint = ["mates"]
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(cat_from, cat_to, interaction)
        )

        interaction_neg = SingleInteraction("test")
        interaction_neg.relationship_constraint = ["-mates"]
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(cat_from, cat_to, interaction_neg)
        )

    def test_parent_child_combo(self):
        # given
        parent = Cat()
        child = Cat(parent1=parent.ID)

        # then
        interaction_cp = SingleInteraction("test")
        interaction_cp.relationship_constraint = ["child/parent"]
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(child, parent, interaction_cp)
        )

        interaction_pc = SingleInteraction("test")
        interaction_pc.relationship_constraint = ["parent/child"]
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(child, parent, interaction_pc)
        )

        self.assertTrue(
            cats_fulfill_single_interaction_constraints(parent, child, interaction_pc)
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(parent, child, interaction_cp)
        )

    def test_rel_values_only_constraint_pos(self):
        # given
        cat_from1 = Cat()
        cat_to1 = Cat()
        low_rel = Relationship(cat_from1, cat_to1)
        low_rel.romance = 10
        low_rel.like = 10
        low_rel.comfort = 10
        low_rel.trust = 10
        low_rel.respect = 10
        cat_from1.relationships[cat_to1.ID] = low_rel

        cat_from2 = Cat()
        cat_to2 = Cat()
        mid_rel = Relationship(cat_from2, cat_to2)
        mid_rel.romance = 50
        mid_rel.like = 50
        mid_rel.comfort = 50
        mid_rel.trust = 50
        mid_rel.respect = 50
        cat_from2.relationships[cat_to2.ID] = mid_rel

        cat_from3 = Cat()
        cat_to3 = Cat()
        high_rel = Relationship(cat_from3, cat_to3)
        high_rel.romance = 90
        high_rel.like = 90
        high_rel.comfort = 90
        high_rel.trust = 90
        high_rel.respect = 90
        cat_from3.relationships[cat_to3.ID] = high_rel

        # then
        for level_list in rel_type_tiers.values():
            for l in level_list:
                high_inter = SingleInteraction("test")
                high_inter.relationship_constraint = [f"{l}_only"]
                mid_inter = SingleInteraction("test")
                mid_inter.relationship_constraint = [f"{l}_only"]
                low_inter = SingleInteraction("test")
                low_inter.relationship_constraint = [f"{l}_only"]
                # last index of the list should be the highest positive
                if l == level_list[-1]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, mid_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, low_inter
                        )
                    )
                # next is middle pos
                elif l == level_list[-2]:
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, mid_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, low_inter
                        )
                    )
                # next is the lowest pos
                elif l == level_list[-3]:
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, mid_inter
                        )
                    )
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, low_inter
                        )
                    )

    def test_rel_values_only_constraint_neg(self):
        # given
        cat_from1 = Cat()
        cat_to1 = Cat()
        mid_rel = Relationship(cat_from1, cat_to1)
        mid_rel.like = -50
        mid_rel.comfort = -50
        mid_rel.trust = -50
        mid_rel.respect = -50
        cat_from1.relationships[cat_to1.ID] = mid_rel

        cat_from2 = Cat()
        cat_to2 = Cat()
        low_rel = Relationship(cat_from2, cat_to2)
        low_rel.like = -10
        low_rel.comfort = -10
        low_rel.trust = -10
        low_rel.respect = -10
        cat_from2.relationships[cat_to2.ID] = low_rel

        cat_from3 = Cat()
        cat_to3 = Cat()
        high_rel = Relationship(cat_from3, cat_to3)
        high_rel.like = -90
        high_rel.comfort = -90
        high_rel.trust = -90
        high_rel.respect = -90
        cat_from3.relationships[cat_to3.ID] = high_rel

        # Skip ROMANCE since it can't go negative (clamped to 0)
        neg_rel_types = {k: v for k, v in rel_type_tiers.items() if k != RelType.ROMANCE}
        for level_list in neg_rel_types.values():
            for l in level_list:
                high_inter = SingleInteraction("test")
                high_inter.relationship_constraint = [f"{l}_only"]
                mid_inter = SingleInteraction("test")
                mid_inter.relationship_constraint = [f"{l}_only"]
                low_inter = SingleInteraction("test")
                low_inter.relationship_constraint = [f"{l}_only"]
                # first index of the list should be the highest negative
                if l == level_list[0]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, mid_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, low_inter
                        )
                    )
                # next is middle negative
                elif l == level_list[1]:
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, mid_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, low_inter
                        )
                    )
                # next is the lowest neg
                elif l == level_list[2]:
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from3, cat_to3, high_inter
                        )
                    )
                    self.assertFalse(
                        cats_fulfill_single_interaction_constraints(
                            cat_from1, cat_to1, mid_inter
                        )
                    )
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from2, cat_to2, low_inter
                        )
                    )

    def test_rel_values_ranged_constraint(self):
        # given
        # pos side
        cat_from_pos = Cat()
        cat_to_pos = Cat()
        high_rel_pos = Relationship(cat_from_pos, cat_to_pos)
        high_rel_pos.romance = 90
        high_rel_pos.like = 90
        high_rel_pos.comfort = 90
        high_rel_pos.trust = 90
        high_rel_pos.respect = 90
        cat_from_pos.relationships[cat_to_pos.ID] = high_rel_pos

        # neg side
        cat_from_neg = Cat()
        cat_to_neg = Cat()
        high_rel_neg = Relationship(cat_from_neg, cat_to_neg)
        high_rel_neg.like = -90
        high_rel_neg.comfort = -90
        high_rel_neg.trust = -90
        high_rel_neg.respect = -90
        cat_from_neg.relationships[cat_to_neg.ID] = high_rel_neg

        # then
        # pos test
        for level_list in rel_type_tiers.values():
            for level in level_list:
                inter = SingleInteraction("test")
                inter.relationship_constraint = [f"{level}"]
                # last index of the list should be the highest positive
                if level == level_list[-1]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_pos, cat_to_pos, inter
                        )
                    )
                # next is middle pos
                elif level == level_list[-2]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_pos, cat_to_pos, inter
                        )
                    )
                # next is the lowest pos
                elif level == level_list[-3]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_pos, cat_to_pos, inter
                        )
                    )

        # neg test - skip ROMANCE since it can't go negative (clamped to 0)
        neg_rel_types = {k: v for k, v in rel_type_tiers.items() if k != RelType.ROMANCE}
        for level_list in neg_rel_types.values():
            for level in level_list:
                inter = SingleInteraction("test")
                inter.relationship_constraint = [f"{level}"]
                # first index of the list should be the highest negative
                if level == level_list[0]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_neg, cat_to_neg, inter
                        )
                    )
                # next is middle neg
                elif level == level_list[1]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_neg, cat_to_neg, inter
                        )
                    )
                # next is the lowest neg
                elif level == level_list[2]:
                    self.assertTrue(
                        cats_fulfill_single_interaction_constraints(
                            cat_from_neg, cat_to_neg, inter
                        )
                    )


class SingleInteractionCatConstraints(unittest.TestCase):
    def test_status(self):
        # given
        warrior = Cat(status_dict={"rank": CatRank.WARRIOR})
        medicine = Cat(status_dict={"rank": CatRank.MEDICINE_CAT})

        # when
        warrior_to_all = SingleInteraction("test")
        warrior_to_all.main_status_constraint = ["warrior"]
        warrior_to_all.random_status_constraint = ["warrior", "medicine cat"]

        warrior_to_warrior = SingleInteraction("test")
        warrior_to_warrior.main_status_constraint = ["warrior"]
        warrior_to_warrior.random_status_constraint = ["warrior"]

        medicine_to_warrior = SingleInteraction("test")
        medicine_to_warrior.main_status_constraint = ["medicine cat"]
        medicine_to_warrior.random_status_constraint = ["warrior"]

        # then
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(
                warrior, warrior, warrior_to_all
            )
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(
                warrior, warrior, warrior_to_warrior
            )
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(
                warrior, warrior, medicine_to_warrior
            )
        )

        self.assertTrue(
            cats_fulfill_single_interaction_constraints(
                warrior, medicine, warrior_to_all
            )
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(
                warrior, medicine, warrior_to_warrior
            )
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(
                warrior, medicine, medicine_to_warrior
            )
        )

        self.assertFalse(
            cats_fulfill_single_interaction_constraints(
                medicine, warrior, warrior_to_all
            )
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(
                medicine, warrior, warrior_to_warrior
            )
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(
                medicine, warrior, medicine_to_warrior
            )
        )

    def test_trait(self):
        # given
        calm = Cat()
        calm.personality.trait = "calm"
        troublesome = Cat()
        troublesome.personality.trait = "troublesome"

        # when
        calm_to_all = SingleInteraction("test")
        calm_to_all.main_trait_constraint = ["calm"]
        calm_to_all.random_trait_constraint = []

        all_to_calm = SingleInteraction("test")
        all_to_calm.main_trait_constraint = ["troublesome", "calm"]
        all_to_calm.random_trait_constraint = ["calm"]

        # then
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(calm, troublesome, calm_to_all)
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(calm, troublesome, all_to_calm)
        )

        self.assertFalse(
            cats_fulfill_single_interaction_constraints(troublesome, calm, calm_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(troublesome, calm, all_to_calm)
        )

        self.assertTrue(
            cats_fulfill_single_interaction_constraints(calm, calm, calm_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(calm, calm, all_to_calm)
        )

    def test_skill(self):
        # given
        hunter = Cat(disable_random=True)
        hunter.skills.primary = Skill(SkillPath.HUNTER, points=9)
        fighter = Cat(disable_random=True)
        fighter.skills.primary = Skill(SkillPath.FIGHTER, points=9)

        # when
        hunter_to_all = SingleInteraction("test")
        hunter_to_all.main_skill_constraint = ["HUNTER,1"]
        hunter_to_all.random_skill_constraint = []

        all_to_hunter = SingleInteraction("test")
        all_to_hunter.main_skill_constraint = ["FIGHTER,1", "HUNTER,1"]
        all_to_hunter.random_skill_constraint = ["HUNTER,1"]

        # then
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(hunter, fighter, hunter_to_all)
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(hunter, fighter, all_to_hunter)
        )

        self.assertFalse(
            cats_fulfill_single_interaction_constraints(fighter, hunter, hunter_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(fighter, hunter, all_to_hunter)
        )

        self.assertTrue(
            cats_fulfill_single_interaction_constraints(hunter, hunter, hunter_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(hunter, hunter, all_to_hunter)
        )

    def test_background(self):
        # given
        clan = Cat()
        clan.backstory = "clanborn"
        half = Cat()
        half.backstory = "halfclan1"

        # when
        clan_to_all = SingleInteraction("test")
        clan_to_all.backstory_constraint = {"m_c": ["clanborn"]}

        all_to_clan = SingleInteraction("test")
        all_to_clan.backstory_constraint = {
            "m_c": ["halfclan1", "clanborn"],
            "r_c": ["clanborn"],
        }

        # then
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(clan, half, clan_to_all)
        )
        self.assertFalse(
            cats_fulfill_single_interaction_constraints(clan, half, all_to_clan)
        )

        self.assertFalse(
            cats_fulfill_single_interaction_constraints(half, clan, clan_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(half, clan, all_to_clan)
        )

        self.assertTrue(
            cats_fulfill_single_interaction_constraints(clan, clan, clan_to_all)
        )
        self.assertTrue(
            cats_fulfill_single_interaction_constraints(clan, clan, all_to_clan)
        )
