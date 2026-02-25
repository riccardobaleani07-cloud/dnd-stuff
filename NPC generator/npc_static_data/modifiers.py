from enums import Size, MagicSource, ArmorType


# That's the map for modify the base attributes
# This file defines stat modifiers using a two-layer system: application mode and expression evaluation.
'''
Each modifier has an "apply" field and an "expr" field.
The "expr" field is a pure expression tree. It does not mutate any values. It evaluates recursively from the innermost operations outward and returns a single result. Expressions may contain:

"const" — a constant value
"stat" — a reference to a stat (including "old_stat" for the current value before modification)
"op?" — an operation applied to a list of values (you write the operation name as the key, and the value can be  asingle value or a list of values, which can themselves be expressions)

Supported expression operations include "add", "inverse" (is like add, but adds the inverse of the value, value*-1), "multiply", "divide", "rd_choice", "max" and "min". Each operation applies only to its listed values (skipping invalid ones) and returns the computed result. Operations do not implicitly reference previous results or external state.
The "apply" field defines how the evaluated expression result is applied to the target stat:

"add" → old_stat += result
"multiply" → old_stat *= result
"subtract" → old_stat -= result
"divide" → old_stat /= result
"replace" → old_stat = result

Evaluation rules:
Expressions are resolved inside → outside.
There is no implicit inclusion of "old_stat" in expressions. It must be referenced explicitly if needed.
Modifier application order is deterministic and follows the order defined in the data.

This separation ensures that expressions remain pure calculations, while the "apply" mode controls how their results affect the stat.
'''
# Example usage:
# {"apply": "replace", "expr": [{"max": [{"const": ArmorType.UNARMORED}, {"stat": "armors"}]}]}
#
# Constants may be numbers, strings, enums, lists, or tuples.
# Tuples are treated as atomic values (single constants), even if they contain multiple components.
# They are mainly used to represent perks with structured data, such as:
#   ("darkvision", 60, "ft")
#   ("hold breath", 15, "minutes")
#
# When multiple tuples with the same perk name (first element) appear in a list,
# they are automatically reduced to the one with the highest numeric value.
# For example:
#   ("darkvision", 60, "ft")
#   ("darkvision", 120, "ft")
# will resolve to:
#   ("darkvision", 120, "ft")
#
# Tuples with different names are treated as distinct perks, even if they are conceptually related:
#   ("darkvision", 60, "ft")
#   ("darkvision (underground only)", 180, "ft")
# These will NOT be merged.
# WARNING: the measurement unit (third element) is NEVER considered in operations, it is mandatory to keep it consistent for the same perk type to ensure coherence. For now, distances are in ft and times are in minutes.

# Notes on things to post format: darkvision ?ft, breath hold ? min, armor (light <- medium ecc)
# Notes on list for post format: random_weapon_list, plantfolk_vulnerability_list, random_tool/kit_list, random_damage_type_list, lycantrope_natural_weapons_list, aasimar_transformation_list, random_skill_list, giant_element_list, draconic_ancestory_list, musical_instrument_list, wizard_cantrip_list, druid_cantrip_list, martial_weapon_list, simple_weapon_list
# When any list is mentioned, it means that it should be rolled from the items in that list, because the list name is a placeholder.

# ToDo: check the list placeholders
wizard_cantrip_list = ["light", "mage hand", "minor illusion", "prestidigitation", "ray of frost", "shocking grasp", "true strike", "chill touch", "dancing lights", "fire bolt", "poison spray", "resistance", "sacred flame", "thorn whip", "vicious mockery"]
martial_weapon_list = []
druid_cantrip_list = []
simple_weapon_list = []
random_skill_list = []
exotic_weapon_list = []
random_weapon_list = [martial_weapon_list, simple_weapon_list, exotic_weapon_list]
random_toolkit_list = []
random_damage_type_list = []


race = { # Common elf contains the complete template
    "Common Elf": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"const": 0}]},
            "ac": {"apply": "add", "expr": [{"const": 0}]},
            "initiative": {"apply": "add", "expr": [{"const": 0}]},
            "speed_bonus": {"walking": {"apply": "add", "expr": [{"const": 0}]}}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.MEDIUM}]} #basic is medium
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 0}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 0}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 0}]},
            "charisma": {"apply": "add", "expr": [{"const": 0}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword","shortsword","longbow","shortbow"]}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.UNARMORED}, {"stat": "armors"}]}]},
            "tools": {"apply": "add", "expr": [{"const": []}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception"]}]},
            "saving_throws": {"apply": "add", "expr": [{"const": []}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"rd_choice": ["wisdom", "intelligence", "charisma"]}]},
            "spell_slots": {1: {"apply": "add", "expr": [{"const": 0}]},
                            2: {"apply": "add", "expr": [{"const": 0}]}},
            "known_spells": {"apply": "add", "expr": [{"const": []}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": []}]},
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": []}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": []}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": []}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Polar Human": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword","spear","harpoon","shortbow"]}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armors"}]}]},
            "tools": {"apply": "add", "expr": [{"const": ["ice fishing tools"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["survival","athletics"]}]},
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "cold"}]}
        }
    },
    "Quarryan Human": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword","light crossbow","flintlock pistol","spear"]}]},
            "tools": {"apply": "add", "expr": [{"const": ["navigation tools"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["deception","persuasion"]}]},
        }
    },
    "South Herian Human": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword","shortsword","longbow","shortbow","rapier"]}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": ["persuasion","insight"]}]},
        }
    },
    "North Herian Human": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword","shortsword","light crossbow","shortbow","hand crossbow"]}]},
            "tools": {"apply": "add", "expr": [{"const": "mason's tools"}]},
            "skills": {"apply": "add", "expr": [{"const": "history"}]}
        }
    },
    "Plains Dorojan Human": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword","shortsword","longbow","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["animal handling","survival"]}]}
        }
    },
    "Mountains Dorojan Human": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["athletics","acrobatics"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "cold"}]}
        }
    },
    "Half-Elf": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": martial_weapon_list}, {"rd_choice": martial_weapon_list}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception", "random_skill_list"]}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": ["charmed (magic-induced sleep)"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Plasmoid": {
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "acid"}]},
            "immunities": {"apply": "add", "expr": [{"const": "poisoned"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"), ("hold breath", 15, "minutes"),
                "amorphous form (can squeeze through 1-inch gaps)",
                "fatural pseudopods (can manipulate objects without hands)"]}]}
        }
    },
    "Spirit": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["scyter","dagger","quarterstaff"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["insight","perception"]}]},
            "saving_throws": {"apply": "add", "expr": [{"const": "wisdom"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "add", "expr": [{"const": "wisdom"}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": druid_cantrip_list}]}
        },

        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "necrotic"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "radiant"}]},
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                ("hold breath", 10, "minutes"),
                "incorporeal movement (can move through creatures and objcts as if they're difficult terrain)",
                ("truesight", 15, "ft"),
                ("spectral sense (sense living creatures)", 60, "ft")
            ]
        }
    },
    "Lopunnie": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"const": 5}]},
            "speed_bonus": {"walking": 
                                {"apply": "add", "expr": [{"const": 5}]}
                            }, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": simple_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "acrobatics"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                "keen hearing",
                "keen smell"]}]}
        }
    },
    "Common Birdling": {
        "core_combat": {
            "speed_bonus": {"walking": {"apply": "add", "expr": [{"const": 5}]},
                            "flying": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": simple_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": "keen sight"}]}
        }
    },
    "Hybrid": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"rd_choice": random_skill_list}, {"rd_choice": random_skill_list}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": 
                "adaptive physiology (once per long rest, gain advantage on one saving throw of choice for the day)"}]}
            
        }
    },
    "Other": {
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"rd_choice": random_skill_list}, {"rd_choice": random_skill_list}]},
            "tools": {"apply": "add", "expr": [{"rd_choice": random_toolkit_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"rd_choice": random_damage_type_list}]}
        }
    },
    "Dark Elf": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": martial_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["Dancing Lights", "Faerie Fire", "Darkness"]}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "sunlight sensitivity"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 120, "ft")}]},
        }
    },
    "Wood Elf": {
        "core_combat": {
            "speed_bonus": {"walking": {"apply": "add", "expr": [{"const": 5}]}}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": martial_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}, {"const": "Mask of the Wild"}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]},
        }
    },
    "Deep Elf": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["light crossbow","spiked ball and chain"]}]},
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "perception(sight) checks done in direct sunlight"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 120, "ft")}]},
        }
    },
    "Moonskin Elf": {
        "core_combat": {
            "speed_bonus": {"walking": {"apply": "add", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["spear","javelin","longbow","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": druid_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "suffocation (it makes you drop to half your hp first, then to 0 hp as normal)"}]},
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}, {"const": ("hold breath", 10, "minutes")}]},
        }
    },
    "Pixie": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"multiply": [{"const": 2}, {"stat": "level"}]}]},
            "speed_bonus": {"flying": {"apply": "replace", "expr": [{"const": 30}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.TINY}]} #basic is medium
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -4}]},
            "dexterity": {"apply": "add", "expr": [{"const": 3}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword", "shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception", "stealth"]}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "invisibility (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "druidcraft"}]}
        }
    },
    "Fairy": {
        "core_combat": {
            "speed_bonus": {"flying": {"apply": "replace", "expr": [{"add": [{"const": 10}, {"stat": "walking"}]}]}}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}, #basic is medium
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword","shield","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": "persuasion"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "faerie fire (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "light"}]}
        },
        "other_info": {
            "add_advantage_on": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]}
        }
    },
    "Firbolg": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"multiply": [{"const": 2}, {"stat": "level"}]}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": simple_weapon_list}, {"rd_choice": simple_weapon_list}, "shield"]},
            "skills": {"apply": "add", "expr": [{"const": "animal handling"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replaace", "expr": [{"const": "wisdom"}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["detect magic (free 1/day)", "disguise self (free 1/day)"]}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["hidden step (free invisibility 1/rest)", ("darkvision", 60, "ft")]}]}
        }
    },
    "Elementalfolk": {
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": "mage armor (free 1/day)"}]}
        }
    },
    "Sylph": { #todo from here: fix the rest
        "core_combat": {
            "speed_bonus": {"walking": 5} #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","simple_weapon_list"],
            "skills": ["acrobatics"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "wisdom",
            "known_spells": ["gust of wind (free 1/day)"],
            "known_cantrips": ["gust"]
        },
        "other_info": {
            "resistances": ["thunder", "lightning"],
            "vulnerabilities": [],
            "other_physical_features": ["slow fall (reduce fall damage by 20ft)"]
        }
    },
    "Dryad": {
        "ability_scores": {
            "constitution": 1,
            "wisdom": 2,
            "charisma": 1
        },
        "proficiencies": {
            "weapons": ["club","quarterstaff","shortbow"],
            "skills": ["nature","survival"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "wisdom",
            "known_spells": ["entangle (free 1/day)"],
            "known_cantrips": ["druidcraft"]
        }
    },
    "Gnome": {
        "core_combat": {
            "size": "small", #basic is medium
        },
        "ability_scores": {
            "dexterity": 1,
            "intelligence": 2
        },
        "proficiencies": {
            "tools": ["tinker's tools"],
            "skills": ["history"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "intelligence",
            "known_spells": ["detect magic (free 1/day)"],
            "known_cantrips": ["minor illusion"]
        },
        "other_info": {
            "immunities": ["charmed (magic-induced sleep)"],
            "other_physical_features": [("darkvision", 60, "ft")]
        }
    },
    "Dwarf": {
        "core_combat": {
            "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": 1,
            "constitution": 2
        },
        "proficiencies": {
            "weapons": ["battleaxe","warhammer","handaxe","shield"],
            "armors": ["light armors","medium armors"],
            "tools": ["smith's tools","brewer's supplies","mason's tools"]
        },
        "other_info": {
            "resistances": ["poison"],
            "other_physical_features": [("darkvision", 60, "ft")]
        }
    },
    "Tabaxi": {
        "core_combat": {
            "speed_bonus": {"walking": 10, "climbing": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": 2,
            "charisma": 1
        },
        "proficiencies": {
            "weapons": ["claws"],
            "skills": ["perception","stealth"]
        },
        "other_info": {
            "immunities": ["charmed (magic-induced sleep)"],
            "other_physical_features": ["feline agility (free dash 1/rest)", ("darkvision", 60, "ft"),
                                        "cat's claws (natural weapons, 1d4 slashing damage)"]
        }
    },
    "Kenku": {
        "ability_scores": {
            "dexterity": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "tools": ["forgery kit", "disguise kit"],
            "skills": ["stealth", "sleight of hand"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "mimicry"]
        }
    },
    "Goliath": {
        "core_combat": {
            "hp": 3
        },
        "ability_scores": {
            "strength": 2,
            "constitution": 2
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","martial_weapon_list","shield"],
            "armors": ["light armors", "medium armors"],
            "skills": ["athletics"]
        },
        "other_info": {
            "resistances": ["cold"],
            "other_physical_features": ["stone's endurance (free stone skin 1/rest)"]
        }
    },
    "Beastfolk": {
        "ability_scores": {
            "strength": 1,
            "dexterity": 1
        },
        "proficiencies": {
            "skills": ["perception"]
        },
        "other_info": {
            "other_physical_features": ["enhanced senses (advantage on perception checks involving smell, sight, or hearing)"]
        }
    },
    "Satyr": {
        "ability_scores": {
            "dexterity": 2,
            "charisma": 1
        },
        "proficiencies": {
            "weapons": ["horns"],
            "tools": ["musical_instrument_list"],
            "skills": ["performance","persuasion"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "known_spells": ["charm person (free 1/day)"],
            "known_cantrips": ["minor illusion"]
        },
        "other_info": {
            "other_physical_features": ["horns (natural weapons, 1d4 bludgeoning damage)"]
        }
    },
    "Bugbear": {
        "core_combat": {
            "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": 2,
            "dexterity": 1,
            "constitution": 1,
            "intelligence": -1,
            "charisma": -1
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","martial_weapon_list"],
            "armors": ["light armors"],
            "skills": ["intimidation", "stealth"]
        },
        "other_info": {
            "other_physical_features": ["long-limbed (reach increased by 5ft)",
                                        "sneaky (advantage on stealth checks in dim light or darkness)"]
        }
    },
    "Sentient Construct": {
        "core_combat": {
            "ac": 2,
            "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "constitution": 2,
            "intelligence": 1,
            "wisdom": 0,
            "charisma": -1
        },
        "proficiencies": {
            "tools": ["artisan's tools"],
            "skills": ["arcana"],
            "saving_throws": []
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "intelligence",
            "spell_slots": {1: 2, 2: 1},
            "known_spells": ["mage armor", "shield"],
            "known_cantrips": ["mending", "mage hand"]
        },
        "other_info": {
            "resistances": ["poison"],
            "immunities": ["diseased"],
            "vulnerabilities": ["cold"],
            "other_physical_features": ["does not need to eat, drink, breathe, or sleep", "can concentrate on spells even while incapacitated"]
        }
    },
    "Giant": {
        "core_combat": {
            "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": "large", #basic is medium
        },
        "ability_scores": {
            "strength": 3,
            "dexterity": -1,
            "constitution": 2
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","martial_weapon_list"],
            "armors": ["light armors","medium armors"],
            "skills": ["athletics"]
        },
        "other_info": {
            "resistances": ["giant_element_list"],
            "other_physical_features": ["enlarged reach (reach increased by 5ft)"]
        }
    },
    "Wolfang": {
        "core_combat": {
            "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": 1,
            "dexterity": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["claws","bite"],
            "skills": ["perception", "survival"]
        },
        "other_info": {
            "resistances": ["diseases"],
            "other_physical_features": [("darkvision", 60, "ft"), "keen hearing", "keen smell",
                                        "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)",
                                        "natural weapons (claws 1d4 slashing damage, bite 1d6 piercing damage)"]
        }
    },
    "Dragonborn": {
        "ability_scores": {
            "strength": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","martial_weapon_list"]
        },
        "other_info": {
            "resistances": ["draconic_ancestory_list"],
            "other_physical_features": ["breath weapon (15ft cone or 30ft line, 2d6 damage, DC 12 dex save for half)"]
        }
    },
    "Half-Dragon": {
        "core_combat": {
            "ac": 2,
            "speed_bonus": {"walking": 0, "flying": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["bite"],
            "skills": ["intimidation"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "immunities": ["draconic_ancestory_list"],
            "other_physical_features": ["breath weapon (15ft cone or 30ft line, 2d6 damage, DC 12 dex save for half)",
                                        "natural weapons (bite 1d8 piercing damage)"]
        }
    },
    "True Dragon": {
        "core_combat": {
            "hp": 30,
            "ac": 3,
            "speed_bonus": {"walking": 10}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": 1,
            "constitution": 2,
            "charisma": 2
        },
        "proficiencies": {
            "weapons": ["breath weapon","claws","bite"],
            "skills": ["intimidation","perception"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "known_spells": ["fear (free 1/day)", "telepathy (at will)"]
        },
        "other_info": {
            "resistances": ["diseases"],
            "immunities": ["draconic_ancestory_list"],
            "other_physical_features": [("darkvision", 120, "ft"),
                                        "breath weapon (30ft cone or 60ft line, 4d6 damage, DC 15 dex save for half)",
                                        "trasformation (can polymorph into dragonish (and back) form gaining flight 60ft, natural weapons (bite 2d10 piercing damage, claw 2d6 slashing damage))",
                                        "legendary resistance (3/rest, can choose to succeed a failed saving throw)"]
        }
    },
    "Kobold": {
        "core_combat": {
            "size": "small", #basic is medium
        },
        "ability_scores": {
            "dexterity": 2,
            "intelligence": 1
        },
        "proficiencies": {
            "weapons": ["dagger","sling","shortbow"],
            "skills": ["random_skill_list"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"),
                                        "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)",
                                        "sunlight sensitivity"]
        }
    },
    "Lizardfolk": {
        "core_combat": {
            "ac": 1,
            "speed_bonus": {"swimming": 30}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "constitution": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "weapons": ["bite","club","javelin","spear"],
            "skills": ["survival","perception"]
        },
        "other_info": {
            "other_physical_features": [("hold breath", 15, "minutes"), "natural weapons (bite 1d6 piercing damage)"]
        }
    },
    "Firefly": {
        "core_combat": {
            "speed_bonus": {"walking": -10, "flying": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": "tiny", #basic is medium
        },
        "ability_scores": {
            "dexterity": 2,
            "charisma": 1
        },
        "proficiencies": {
            "weapons": ["sting"],
            "skills": ["stealth"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "known_spells": ["produce flame (free at will)"],
            "known_cantrips": ["faerie fire"]
        },
        "other_info": {
            "resistances": ["fire"],
            "vulnerabilities": ["cold"],
            "other_physical_features": [("darkvision", 60, "ft"), "bioluminescence (can emit bright light in 10ft radius and dim light for additional 10ft)"]
        }
    },
    "Pale Knight": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]},
            "initiative": {"apply": "subtract", "expr": [{"stat": "dexterity_mod"}]},
            "speed_bonus": {"walking": -10},  # 20 ft base
            "size": "small"
        },
        "ability_scores": {
            "dexterity": -1,
            "constitution": +2,
            "intelligence": +1,
            "wisdom": +1
        },
        "proficiencies": {
            "weapons": ["dagger", "rapier"],
            "tools": ["masons_tools"],
            "skills": ["perception", "deception"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["druid_cantrip_list"]
        },
        "other_info": {
            "resistances": ["necrotic", "poison"],
            "add_advantage_on": ["petrified"],
            "other_physical_features": [
                "blind (cannot see normally)",
                "telepathy 60ft (Paladrin only)",
                "thermal vision 10ft",
                "dark sustenance (does not need to eat or drink normally)",
                "mute (doesn't speak normally)"
            ]
        }
    },
    "Lost Goblin": {
        "core_combat": {
            "size": "small", #basic is medium
        },
        "ability_scores": {
            "dexterity": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "weapons": ["shortsword", "shortbow"],
            "skills": ["insight","intimidation"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "nimble escape (can take disengage or hide action as a bonus action on each of its turns)"]
        }
    },
    "Hobgoblin": {
        "ability_scores": {
            "strength": 1,
            "constitution": 1,
            "intelligence": 2
        },
        "proficiencies": {
            "weapons": ["martial_weapon_list"],
            "skills": ["history","intimidation"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "martial advantage (when it or an ally within 5ft attacks with a martial weapon, can roll with advantage)"]
        }
    },
    "Lost Sea Goblin": {
        "core_combat": {
            "speed_bonus": {"walking": -5, "swimming": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": "small", #basic is medium
        },
        "ability_scores": {
            "dexterity": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "weapons": ["trident", "shortbow"],
            "skills": ["athletics", "insight"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "wisdom",
            "known_spells": ["minor illusion (free 4/day)"]
            },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), ("hold breath", 30, "minutes")]
        }
    },
    "Mushroomfolk": {
        "core_combat": {
            "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": "small", #basic is medium
        },
        "ability_scores": {
            "constitution": 2,
            "wisdom": 1
        },
        "proficiencies": {
            "weapons": ["unarmed strike"],
            "skills": ["nature", "medicine"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "wisdom",
            "known_spells": ["fungal spores (free 2/day)"],
            "known_cantrips": ["druid_cantrip_list"]
        },
        "other_info": {
            "resistances": ["poison"],
            "other_physical_features": ["keen smell"]
        }
    },
    "Ogre": {
        "core_combat": {
            "ac": 2,
            "speed_bonus": {"walking": 10}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
            "size": "large", #basic is medium
        },
        "ability_scores": {
            "strength": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["unarmed strike", "greatclub"],
            "skills": ["intimidation"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                        "fists of steel (natural weapons, 1d8 bluedgeoning damage)"]
        }
    },
    "Half-Ogre": {
        "ability_scores": {
            "strength": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["unarmed strike", "greatclub"],
            "skills": ["intimidation", "athletics"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                        "heavy fists (natural weapons, 1d6 bluedgeoning damage)"]
        }
    },
    "Insectoid": {
        "core_combat": {
            "ac": +3
        },
        "ability_scores": {
            "dexterity": +2
        },
        "proficiencies": {
            "skills": ["perception"]
        },
        "other_info": {
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "electroreception (sense electrical fields within 30ft)",
                "compound eyes or mandibles",
                "insectoid physiology"
            ]
        }
    },
    "Grung": {
        "core_combat": {
            "speed_bonus": {"climbing": 25},
            "size": "small"
        },
        "ability_scores": {
            "dexterity": +2,
            "constitution": +1
        },
        "proficiencies": {
            "skills": ["athletics"]
        },
        "other_info": {
            "resistances": ["poison"],
            "immunities": [],
            "vulnerabilities": [],
            "add_advantage_on": ["poisoned"],
            "add_disadvantage_on": [],
            "other_physical_features": [
                "amphibious (can breathe air and water)",
                "poisonous skin (contact poison, DC 12 con save or be poisoned for 1 min)",
                "standing leap (long jump 25ft, high jump 15ft without run-up)"
            ]
        }
    },
    "Kling": {
        "core_combat": {
            "speed_bonus": {"swimming": 20},
            "size": "small"
        },
        "ability_scores": {
            "dexterity": +2,
            "intelligence": +1
        },
        "proficiencies": {
            "tools": ["tinkers_tools"],
            "skills": ["sleight_of_hand", "survival"]
        },
        "other_info": {
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "amphibious (can breathe air and water)",
                "scavenger culture (advantage on checks to find usable materials)"
            ]
        }
    },
    "Halfling": {
        "core_combat": {
            "speed_bonus": {"walking": -5},
            "size": "small"
        },
        "ability_scores": {
            "dexterity": 2,
            "charisma": 1
        },
        "proficiencies": {
            "skills": ["stealth"]
        },
        "other_info": {
            "add_advantage_on": ["frightened"],
            "other_physical_features": ["lucky (reroll a nat 1 on a d20)", "nimbleness (you can move through a creature bigger than you)"]
        }
    },
    "Orc": {
        "ability_scores": {
            "strength": 2,
            "constitution": 1
        },
        "proficiencies": {
            "weapons": ["greataxe", "javelin"]
        },
        "other_info": {
            "other_physical_features": [("darkvision", 60, "ft"), "powerful build (counts as one size larger for carrying capacity and push/drag/lift"]
        }
    },
    "Plantfolk": {
        "core_combat": {
            "speed_bonus": {"climbing": 10}
        },
        "ability_scores": {
            "dexterity": 1,
            "constitution": 2,
            "wisdom": 2,
        },
        "proficiencies": {
            "weapons": ["dagger", "quarterstaff", "sickle"],
            "tools": ["herbalism kit", "alchemist supplies"],
            "skills": ["nature", "perception", "survival"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["entangle (free at will)", "goodberry (free 1/day)"],
            "known_cantrips": ["druidcraft"]
        },
        "other_info": {
            "resistances": ["poison"],
            "vulnerabilities": ["plantfolk_vulnerability_list"],
            "add_advantage_on": ["nature", "herbalism kit", "prone", "stealth (in foliage)"]
        }
    },
    "Tiefling": {
        "ability_scores": {
            "intelligence": 1,
            "charisma": 2
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["thaumaturgy"],
            "known_spells": ["disguise self (free 1/day)", "hellish rebuke (free 1/day)"]
        },
        "other_info": {
            "resistances": ["fire"],
            "other_physical_features": [("darkvision", 60, "ft")]
        }
    },
    "Demonoid": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {"flying": 15}
        },
        "ability_scores": {
            "strength": 1,
            "dexterity": 1,
            "constitution": 1,
            "charisma": 1
        },
        "proficiencies": {
            "weapons": ["dagger", "longsword", "shortsword"],
            "skills": ["intimidation", "arcana"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["hellish rebuke (free 1/day)"],
            "known_cantrips": ["thaumaturgy", "wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["fire"],
            "other_physical_features": [
                "demonic heritage (can recall demonic powers, manifests as luminescent horns, wings or tail)",
                ("darkvision", 60, "ft")
            ]
        },
    },
    "Yuan-Ti": {
        "ability_scores": {
            "intelligence": 1,
            "charisma": 2
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["poison spray"],
            "known_spells": ["suggestion (free 1/day)"]
        },
        "other_info": {
            "immunities": ["poison"],
            "other_physical_features": [("darkvision", 60, "ft"), "magic resistance (advantage vs spells)"]
        }
    },
    "Demon": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"op": "multiply", "value": [{"stat": "proficiency_bonus"}, {"stat": "level"}]}]},
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {"flying": 30}
        },
        "ability_scores": {
            "strength": 2,
            "charisma": 2
        },
        "proficiencies": {
            "weapons": ["dagger", "longsword", "shortsword"],
            "skills": ["intimidation", "arcana"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["darkness (free 1/day)", "teleport (free 1/day)", "hellish rebuke (free 1/day)"],
            "known_cantrips": ["thaumaturgy", "wizard_cantrip_list", "message"]
        },
        "other_info": {
            "resistances": ["fire", "cold", "lightning", "force"],
            "immunities": ["charmed", "frightened"],
            "vulnerabilities": ["radiant", "necrotic"],
            "other_physical_features": [("darkvision", 120, "ft"),
                                        "regeneration (regain 5 HP at the start of its turn if it has at least 1 HP)",
                                        "demonic taunt (once per turn, can deal extra 7 (2d6) necrotic damage to a creature it hits with a weapon attack)",
                                        "true sight 45ft"]
        }
    },
    "Salamanderman": {
        "core_combat": {
            "speed_bonus": {"swimming": 20}
        },
        "ability_scores": {
            "strength": 1,
            "dexterity": 2,
        },
        "proficiencies": {
            "weapons": ["dagger", "shortsword"],
            "skills": ["survival", "nature"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["fire"],
            "add_advantage_on": ["athletics (when balance is needed)"],
            "other_physical_features": [
                "regenerative skin (heals minor wounds faster for 1d4 HP at the start of its turn)",
                "tail can be used for balance or minor attacks (1d4 bludgeoning)",
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Oni": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}]}
        },
        "ability_scores": {
            "strength": +2,
            "dexterity": +1,
            "charisma": +1
        },
        "proficiencies": {
            "weapons": ["longsword", "katana", "shortsword"],
            "skills": ["intimidation"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["fire bolt"]
        },
        "other_info": {
            "resistances": ["fire"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "horns (natural weapons, 1d6 piercing damage)",
                "innate flame affinity (fire spells are deep red or purple)"
            ]
        }
    },
    "Kijin": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}, {"const": 2}]},
            "size": "medium"
        },
        "ability_scores": {
            "dexterity": +2,
            "intelligence": +1,
            "wisdom": +1
        },
        "proficiencies": {
            "weapons": ["longsword", "katana", "longbow"],
            "skills": ["arcana"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["mage armor (free at will)", "detect magic (free at will)"],
            "known_cantrips": ["wizard_cantip_list"]
        },
        "other_info": {
            "resistances": ["fire"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "magic vision (can see magic energy and auras)"
            ]
        }
    },
    "Majin": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}, {"const": 5}]},
            "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]}
        },
        "ability_scores": {
            "strength": +2,
            "dexterity": +2,
            "charisma": +2
        },
        "proficiencies": {
            "skills": ["perception", "intimidation"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["mage armor (free at will)", "detect magic (free at will)"],
            "known_cantrips": ["wizard_cantrip_list", "wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["fire", "necrotic"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "thermal vision 10ft",
                "tremorsense 10ft",
                "heightened senses (advantage on perception checks involving smell, sight, or hearing)",
                "overwhelming presence (once per day, force all creatures within 30ft that can see you to make a DC 15 wisdom saving throw or be frightened for 1 minute)"
            ]
        }
    },
    "Strix": {
        "ability_scores": {
            "intelligence": +2,
            "wisdom": +1,
            "constitution": -1
        },
        "proficiencies": {
            "skills": ["insight", "arcana"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["psychic"],
            "add_advantage_on": ["charmed", "frightened"],
            "other_physical_features": [
                "tentacle manifestation (can grow/absorb grown tentacles from the back)",
                "grown tentacles can manipulate objects but cannot wield weapons",
                "self-replication capable (rare, slow process)"
            ]
        }
    },
    "Nightmare": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
        },
        "ability_scores": {
            "strength": -1,
            "dexterity": 1,
            "intelligence": 1,
            "charisma": 2
        },
        "proficiencies": {
            "skills": ["deception", "insight"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "spell_slots": {1: 2, 2: 2},
            "known_spells": ["sleep (free 1/day)", "cause fear (free 1/day)"],
            "known_cantrips": ["minor illusion", "friendship"]
        },
        "other_info": {
            "resistances": ["psychic"],
            "immunities": ["magical sleep"],
            "add_advantage_on": ["feared"],
            "other_physical_features": [
                "shapeshifter (humanoid forms only)",
                "nightmare induction (creatures that sleep within 30ft may suffer disturbing dreams and not gain benefits of a long rest at your discrection)",
                "dream-feeding (regain 2d6 hp after inducing a nightmare)"
            ]
        }
    },
    "Celestial": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "wisdom_mod"}]},
            "speed_bonus": {"flying": 15}
        },
        "ability_scores": {
            "constitution": 1,
            "wisdom": 1,
            "charisma": 2
        },
        "proficiencies": {
            "weapons": ["simple_weapon_list","martial_weapon_list"],
            "skills": ["insight"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["cure wounds (free 1/day)", "protection from evil and good (free 1/day)"],
            "known_cantrips": ["thaumaturgy", "light"]
        },
        "other_info": {
            "resistances": ["radiant"],
            "add_advantage_on": ["feared"],
            "other_physical_features": [
                "celestial heritage (can manifest wings of light, halo or radiant tail)",
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Angel": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"op": "multiply", "value": [{"stat": "proficiency_bonus"}, {"stat": "level"}]}]},
            "ac": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"flying": 30}
        },
        "ability_scores": {
            "strength": 2,
            "constitution": 2,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 2
        },
        "proficiencies": {
            "weapons": ["spear", "longsword", "longbow", "simple_weapon_list"],
            "armors": ["light", "medium", "heavy"],
            "tools": [],
            "skills": ["insight", "arcana"],
            "saving_throws": ["wisdom", "charisma"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["shield of faith (free at will)", "lesser restoration (free 1/day)"],
            "known_cantrips": ["light", "thaumaturgy", "wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["radiant", "necrotic"],
            "immunities": ["charmed", "frightened"],
            "other_physical_features": [
                "divine regeneration (regain 5 hp at the start of its turn if it has at least 1 hp)",
                "angelic touch (heals a creature or mends an object for 2d4 + 3 hp as an action)",
                ("darkvision", 120, "ft"),
                ("truesight", 30, "ft")
            ]
        }
    },
    "Aarakocra": {
        "core_combat": {
            "speed_bonus": {"flying": 50} #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": 2,
            "wisdom": 1
        },
        "other_info": {
            "other_physical_features": ["keen sight (advantage on perception checks that rely on sight)", "talons (natural weapons, 1d4 slashing)"]
        }
    },
    "Aasimar": {
        "ability_scores": {
            "charisma": +2,
            "wisdom": +1
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["light"]
        },
        "other_info": {
            "resistances": ["radiant", "necrotic"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "celestial legacy (aasimar_transformation_list)"
            ]
        }
    },
    "Moonling": {
        "core_combat": {
            "speed_bonus": {"walking": -5},
            "size": "small"
        },
        "ability_scores": {
            "strength": -1,
            "dexterity": +2,
            "intelligence": +1,
            "wisdom": +2
        },
        "proficiencies": {
            "skills": ["survival", "perception"]
        },
        "magic": {
            "magic_source": None
        },
        "other_info": {
            "other_physical_features": [
                "light-perception vision (cannot see shapes or colors, only light intensity; blinded by magical darkness)",
                "tremorsense 30ft",
                "magnetic sense 60ft",
                "keen hunter (advantage on survival checks to track creatures)",
                "generational grudge (once a Moonling has been harmed by a creature, that creature has disadvantage on charisma checks against Moonlings of the same community)"
            ]
        }
    },
    "Foxling": {
        "ability_scores": {
            "dexterity": +2,
            "charisma": +1
        },
        "core_combat": {
            "speed": +5
        },
        "proficiencies": {
            "weapons": ["crossbows", "polearms", "hand fans"],
            "skills": ["stealth", "insight"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["minor illusion"]
        },
        "other_info": {
            "senses": [("darkvision", 60, "ft")],
            "other_physical_features": [
                "fox senses (recognizes individuals by scent and magical trace)",
                "heat sensitivity (can detect warm creatures within 10ft)",
                "natural agility (advantage on dexterity saving throws against effects you can see)"
            ]
        }
    },
    "Shadowkin": {
        "core_combat": {
            "ac": +4
        },
        "ability_scores": {
            "strength": +1,
            "dexterity": +1,
            "charisma": +1
        },
        "proficiencies": {
            "armors": ["light", "medium", "heavy"],
            "weapons": ["simple_weapon_list","martial_weapon_list","shield"],
            "skills": ["intimidation"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["necrotic"],
            "add_advantage_on": ["frightened"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "armor shell (can inhabit incomplete or abandoned armor that drops if defeated)"
            ]
        }
    },
    "Wisp": {
        "core_combat": {
            "ac": +5,
            "initiative": +2,
            "speed_bonus": {"flying": 30},
            "size": "small"
        },
        "ability_scores": {
            "strength": -2,
            "dexterity": 2,
            "constitution": -1,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 2
        },
        "proficiencies": {
            "skills": ["arcana", "stealth"],
            "saving_throws": ["dexterity", "wisdom"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "spell_slots": {1: 2},
            "known_spells": ["light (free 1/day)", "mage hand (free 2/day)", "minor illusion (free 1/day)"],
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["lightning", "poison"],
            "vulnerabilities": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"],
            "add_advantage_on": ["stealth (in dim light or darkness)"],
            "other_physical_features": [
                "incorporeal form (can pass through small openings, 1 inch wide, cannot wear armor or carry objects)",
                "glowing body (light radius 10ft, can dim at will)",
                "possessive ability (can attempt to possess a willing or helpless humanoid once per short rest, duration 1 minute)",
                "hovering flight (can hover and fly)"
            ]
        }
    },
    "Voidling": {
        "core_combat": {
            "speed_bonus": {"walking": -5},
            "size": "small"
        },
        "ability_scores": {
            "strength": -2,
            "dexterity": +2,
            "intelligence": +1,
            "charisma": +1
        },
        "proficiencies": {
            "weapons": ["dagger", "rapier"],
            "tools": ["tinkers_tools", "jewelers_tools"],
            "skills": ["stealth"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["wizard_cantrip_list"]
        },
        "other_info": {
            "resistances": ["necrotic"],
            "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
            "other_physical_features": [
                ("darkvision", 60, "ft"),
                "telepathy 60ft (Voshedi only)",
                "dark sustenance (does not need to eat or drink normally)",
                "darknesssynthesis (inverted photosynthesis)",
                "mute (doesn't speak normally)"
            ]
        }
    },
    "Lycanthrope": {
        "core_combat": {
            "ac": +2
        },
        "ability_scores": {
            "strength": +2,
            "constitution": +1
        },
        "proficiencies": {
            "skills": ["perception"]
        },
        "other_info": {
            "resistances": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"],
            "immunities": [],
            "vulnerabilities": ["silvered weapons"],
            "add_advantage_on": ["perception (smell)"],
            "add_disadvantage_on": [],
            "other_physical_features": [
                "hybrid nightime transformation (can transform into hybrid form only at night; transformation is more severe the more the moon is visible)",
                "natural weapons (lycantrope_natural_weapons_list)"
            ]
        }
    },
    "Sentient Undead": {
        "ability_scores": {
            "constitution": 2,
            "intelligence": 1,
            "charisma": -1
        },
        "proficiencies": {
            "skills": ["history"]
        },
        "other_info": {
            "resistances": ["necrotic"],
            "immunities": ["poison", "disease"],
            "vulnerabilities": ["radiant"],
            "add_advantage_on": ["feared"],
            "add_disadvantage_on": ["charisma checks (dealing with the living)"],
            "other_physical_features": [
                "does not need food or air"
            ]
        }
    },
    "Starborn": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
            "initiative": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"walking": 10, "flying": 20},
        },
        "ability_scores": {
            "strength": -1,
            "dexterity": 1,
            "constitution": -1,
            "intelligence": 3,
            "wisdom": 1,
            "charisma": 3
        },
        "proficiencies": {
            "skills": ["arcana", "history", "persuasion"],
            "saving_throws": ["intelligence", "charisma", "constitution"]
        },
        "magic": {
            "magic_source": "Innate",
            "spellcasting_ability": "charisma",
            "spell_slots": {
                1: 4,
                2: 3,
                3: 3,
                4: 3,
                5: 3,
                6: 2,
                7: 2,
                8: 2,
                9: 2
            },
            "known_spells": ["wish", "meteor swarm", "plane shift", "disintegrate", "magic missle", "counterspell", "detect magic"],
            "known_cantrips": ["light", "fire bolt"]
        },
        "other_info": {
            "resistances": ["radiant", "force"],
            "immunities": ["diseased", "exhaustion (nonmagical)"],
            "vulnerabilities": ["psychic"],
            "other_physical_features": [
                "stellar core (no need for air, food or sleep)",
                "energy dependency (at 16 spell slots or less, cannot fly and all the resistances are lost; at 5 spell slots or less gains mortal needs; at 0 suffer from 1d8 + 2 damage for every half hour without sleep)",
                "slow recharge (regain spell slots only up to the 4th level after a long rest, plus 2 additional slot of the lowest level spent over 5th)",
                "half-familiar (you can bond with an other humanoid with a ritual: Stellar Covenant, 9th-level transmutation (ritual), Casting Time: 24 hours, Range: Touch, Components: V, S, M (a focus attuned to stellar energy worth at least 10,000 gp, consumed), Duration: Until broken, Description: this ritual forges a one-way metaphysical bond between a Starborn and a single willing creature, designating that creature as the Starborn's Chosen. In exchange of a predefined thing, the Chosen can order the Starborn to act. The pact can be broken by both if one is not fullfilling the pact's terms. The pact is exclusive.)",
                "loyal bond (can cast spells above the 4th level only for a chosen bonded creature)",
                "restricted attunement (only one weapon or focus)",
                "fatigue sensitivity (disadvantage on constitution saving throws against exhaustion effects)",
                ("darkvision", 120, "ft")
            ]
        }
    },
    "Crystalborn": {
        "core_combat": {
            "size": "small"
        },
        "ability_scores": {
            "strength": -2,
            "constitution": 1,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1
        },
        "proficiencies": {
            "tools": ["artisan_tools"],
            "skills": ["arcana", "perception"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["light"]
        },
        "other_info": {
            "resistances": ["psychic"],
            "vulnerabilities": ["thunder"],
            "add_advantage_on": ["arcana"],
            "add_disadvantage_on": ["stealth"],
            "other_physical_features": [
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Changeling": {
        "ability_scores": {
            "charisma": +2,
            "dexterity": +1
        },
        "proficiencies": {
            "skills": ["deception"]
        },
        "other_info": {
            "add_advantage_on": ["deception (related to identity)"],
            "other_physical_features": [
                "shapechanger (humanoid appearance only)"
            ]
        }
    },
    "True Vampire": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"stat": "constitution_mod"}, {"const": 2}]},
            "ac": {"apply": "add", "expr": [{"const": 1}]},
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {
                "walking": +5,
                "flying": 30
            }
        },
        "ability_scores": {
            "strength": +1,
            "dexterity": +2,
            "constitution": +1,
            "charisma": +2
        },
        "proficiencies": {
            "skills": ["perception", "persuasion"]
        },
        "magic": {
            "magic_source": None
        },
        "other_info": {
            "resistances": ["necrotic"],
            "immunities": ["diseases", "poison", "exhaustion (non-magical)", "aging effects"],
            "add_advantage_on": ["death effects"],
            "add_disadvantage_on": ["perception (smell, when garlic is in 5ft)"],
            "other_physical_features": [
                ("darkvision", 120, "ft"),
                "enhanced senses (advantage on perception checks relying on smell, taste, or hearing)",
                "no heartbeat",
                "does not need to breathe",
                "regeneration (regain hit points equal to proficiency bonus at the start of turn if at least 1 HP and has consumed blood in the last 24 hours)",
                "phase step (once per short rest, can move through solid objects up to 10ft as difficult terrain)",
                "flight (hover; cannot wear heavy armor)",
                "mist form (once per long rest, transform into mist for 1 minute; cannot attack or cast spells, can pass through tiny openings, speed becomes flying 40ft)",
                "no reflection (mirrors and reflective surfaces do not show the vampire)"
            ]
        }
    },
    "Spectre": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"flying": 30}
        },
        "ability_scores": {
            "strength": -2,
            "dexterity": 1,
            "constitution": -2,
            "intelligence": 1,
            "wisdom": 1,
        },
        "proficiencies": {
            "skills": ["perception", "stealth"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["thaumaturgy"]
        },
        "other_info": {
            "resistances": ["necrotic", "psychic"],
            "immunities": ["poison", "diseased", "poisoned"],
            "vulnerabilities": ["radiant"],
            "add_advantage_on": ["stealth"],
            "other_physical_features": [
                "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Triton": {
        "core_combat": {
            "speed_bonus": {"swimming": 30}
        },
        "ability_scores": {
            "strength": +1,
            "constitution": +1,
            "charisma": +1
        },
        "proficiencies": {
            "weapons": ["trident", "spear"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["fog cloud (free 1/day)"]
        },
        "other_info": {
            "resistances": ["cold"],
            "other_physical_features": [
                "amphibious (breathe air and water)",
                "aquatic adaptation (water contact reveals scale skin, gills, webbed fingers/toes)",
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Mermaid": {
        "core_combat": {
            "speed_bonus": {"walking": -20, "swimming": 45}
        },
        "ability_scores": {
            "constitution": 1,
            "charisma": 2
        },
        "magic": {
            "magic_source": "Innate",
            "known_cantrips": ["shape water"],
            "known_spells": ["water breathing (free at will)"]
        },
        "other_info": {
            "other_physical_features": ["amphibious (breath air and water)"]
        }
    },
    "Nymph": {
        "ability_scores": {
            "wisdom": 1,
            "charisma": 2
        },
        "proficiencies": {
            "saving_throws": ["dexterity"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["charm person (free 3/day)", "entangle (free at will)"]
        },
        "other_info": {
            "add_advantage_on": ["charmed"]
        }
    },
    "Turtoid": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 1}]},
            "initiative": {"apply": "subtract", "expr": [{"stat": "dexterity_mod"}]},
            "speed_bonus": {"walking": -5, "swimming": 15}
        },
        "ability_scores": {
            "dexterity": -1,
            "constitution": 2,
            "wisdom": 1,
        },
        "proficiencies": {
            "weapons": ["club", "spear"],
            "skills": ["survival"],
        },
        "other_info": {
            "resistances": ["cold"],
            "add_advantage_on": ["strength (carrying or pushing)"],
            "add_disadvantage_on": ["dexterity saving throws"],
            "other_physical_features": [
                "tough shell (can retract as a bonus action to increase AC by 3)",
                ("hold breath", 15, "minutes")
            ]
        }
    },
    "Gooba": {
        "core_combat": {
            "speed_bonus": {"walking": -10, "swimming": 30}
        },
        "ability_scores": {
            "dexterity": +2,
            "constitution": +2,
            "intelligence": +1,
            "charisma": -1
        },
        "proficiencies": {
            "skills": ["stealth", "athletics"]
        },
        "magic": {
            "magic_source": None
        },
        "other_info": {
            "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
            "other_physical_features": [
                "amphibious (can breathe air and water)",
                "dehydration weakness (after 24 hours without at least 2 hours submerged in water, gain one level of exhaustion per day)",
                "tentacular limbs (can interact with objects, grapple, or climb using tentacles; advantage on grapple checks)",
                "chromatic shift (can change skin color briefly; gains advantage on stealth checks)",
                "ink burst (once per short rest, release ink in a 10ft radius underwater, heavily obscured for 1 minute)",
                ("darkvision", 60, "ft")
            ]
        }
    },
    "Banshee": {
        "core_combat": {
            "speed_bonus": {"flying": 30}
        },
        "ability_scores": {
            "strength": -1,
            "constitution": -1,
            "wisdom": 1,
            "charisma": 3
        },
        "proficiencies": {
            "skills": ["intimidation", "performance"]
        },
        "magic": {
            "magic_source": "Innate",
            "known_spells": ["fear (free 1/day)", "silent image (free 1/day)"],
            "known_cantrips": ["vicious mockery"]
        },
        "other_info": {
            "resistances": ["necrotic", "psychic"],
            "immunities": ["poison", "charmed", "poisoned", "frightened"],
            "vulnerabilities": ["radiant"],
            "add_advantage_on": ["intimidation"],
            "add_disadvantage_on": ["concentration (for maintaining spells)"],
            "other_physical_features": [
                "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                "wail resonance (once per long rest, emit a wail causing all creatures within 30ft to make a DC 15 constitution saving throw or take 4d6 psychic damage and be frightened for 1 minute; half damage and no fright on successful save)",
                ("darkvision", 60, "ft")
            ]
        }
    }
}

subtype = {
        "Shell": {
            "other_info": {
                "resistances": ["force"],
                "other_physical_features": [
                    "shell recall (1/day, grant temporary protection: any creature within 10ft gain 1d8 temporary hp for the next turn if starts the turn there)"
                ]
            }
        },
        "Lush": {
            "ability_scores": {
                "charisma": 1
            },
            "other_info": {
                "resistances": ["poison"],
                "other_physical_features": [
                    "lush recall (1/day, restore vitality in area: any object suffers from mending effect, every creature heal for 1d4 hp if starts the turn there)"
                ]
            }
        },
        "Grace": {
            "ability_scores": {
                "wisdom": 1,
                "constitution": 1
            },
            "other_info": {
                "resistances": ["cold"],
                "other_physical_features": [
                    "frost aura (standing still, can freeze up surroundings, up to freezing water and brittle metal in a 5ft radius, 1/day)"
                ]
            }
        },
        "Ghost": {
            "core_combat": {
                "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
                "initiative": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
                "speed_bonus": {"flying": 30}
            },
            "ability_scores": {
                "strength": -3,
                "dexterity": 2,
                "constitution": -3,
                "intelligence": 1,
                "wisdom": 1,
                "charisma": 1
            },
            "other_info": {
                "resistances": ["necrotic", "nonmagical weapons"],
                "vulnerabilities": ["radiant"],
                "other_physical_features": [
                    "incorporeal movement (can move through objects as if they're difficult terrain)",
                    "cannot wear armor"
                ]
            }
        },
        "Skeleton": {
            "ability_scores": {
                "strength": -1,
                "dexterity": 2,
                "constitution": -1,
                "charisma": -1
            },
            "other_info": {
                "resistances": ["piercing"],
                "vulnerabilities": ["bludgeoning"],
                "other_physical_features": [
                    "does not bleed"
                ]
            }
        },
        "Zombie": {
            "core_combat": {
                "hp": {"apply": "add", "expr": [{"stat": "constitution_mod"}]},
                "initiative": {"apply": "subtract", "expr": [{"stat": "dexterity_mod"}]},
                "speed_bonus": {"walking": -5}
            },
            "ability_scores": {
                "strength": 1,
                "dexterity": -2,
                "constitution": 2,
                "intelligence": -1,
                "charisma": -1
            },
            "other_info": {
                "vulnerabilities": ["fire"],
                "other_physical_features": [
                    "relentless endurance (first time reduced to 0 hp, drop to 1 instead, once per long rest)"
                ]
            }
        },
        "Cerberian": {
            "ability_scores": {"strength": 1, "constitution": 1},
            "other_info": {
                "other_physical_features": [
                    "heat aura (standing still, can warm surroundings, up to melting metal in a 5ft radius, 1/day)"
                ]
            }
        },
        "Blood Beat": {
            "ability_scores": {"charisma": 2},
            "other_info": {
                "other_physical_features": [
                    "blood manipulation (can control blood in a small area, up to 15ft radius, 1/day)"
                ]
            }
        },
        "Wither": {
            "ability_scores": {"wisdom": 1, "constitution": 1},
            "other_info": {
                "other_physical_features": [
                    "life drain (1/day, can recall powers to drain life in a area of 10ft radius: any creature that starts its turn there takes 1d4 necrotic damage and you heal for half the amount)"
                ]
            }
        },
        "Steam": {
            "ability_scores": {
                "constitution": +1,
                "wisdom": +1
            },
            "other_info": {
                "resistances": ["fire"],
                "add_advantage_on": ["concentration (for maintaining spells)"],
                "other_physical_features": [
                    "obscuring mist (can lightly obscure a 10ft radius once per long rest)"
                ]
            }
        },
        "Dust": {
            "ability_scores": {
                "dexterity": +2
            },
            "other_info": {
                "resistances": ["poison"],
                "other_physical_features": [
                    "dust cloud body (can impose disadvantage on one ranged attack against you per short turn)"
                ]
            }
        },
        "Smoke": {
            "ability_scores": {
                "dexterity": +1,
                "charisma": +1
            },
            "other_info": {
                "resistances": ["fire"],
                "other_physical_features": [
                    "smoky form (can lightly obscure a 5ft radius around self)",
                    "choking presence (creatures adjacent have disadvantage on perception checks relying on sight)"
                ]
            }
        },
        "Lava": {
            "ability_scores": {
                "strength": +1,
                "charisma": +1
            },
            "core_combat": {
                "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}, {"const": 2}]}
            },
            "proficiencies": {
                "skills": ["intimidation"]
            },
            "other_info": {
                "resistances": ["fire"],
                "other_physical_features": [
                ]
            }
        },
        "Ice": {
            "ability_scores": {
                "dexterity": +1
            },
            "other_info": {
                "immunities": ["cold"],
                "vulnerabilities": ["fire"],
                "other_physical_features": [
                    "frozen skin (creatures grappling you take 1 cold damage per round)"
                ]
            }
        },
        "Mud": {
            "ability_scores": {
                "constitution": +1,
                "strength": +1
            },
            "core_combat": {
                "speed_bonus": {"walking": -10}
            },
            "other_info": {
                "resistances": ["poison"],
                "add_advantage_on": ["poisoned", "prone"],
                "other_physical_features": [
                    "difficult terrain affinity (ignores non-magical mud-based difficult terrain)"
                ]
            }
        },
        "Earth": {
            "ability_scores": {
                "strength": +1
            },
            "proficiencies": {
                "skills": ["animal handling", "nature"]
            },
            "other_info": {
                "resistances": ["poison"],
                "other_physical_features": [
                    "tremorsense 10ft"
                ]
            }
        },
        "Wind": {
            "ability_scores": {
                "dexterity": +1
            },
            "core_combat": {
                "speed_bonus": {"walking": +5}
            },
            "other_info": {
                "resistances": ["force"],
                "vulnerabilities": ["bludgeoning"],
                "other_physical_features": [
                    "flickering form (disadvantage on opportunity attacks against you)",
                    "lightweight body (can hover 5ft off the ground)"
                ]
            }
        },
        "Fire": {
            "ability_scores": {
                "charisma": +1
            },
            "other_info": {
                "immunities": ["fire"],
                "vulnerabilities": ["cold"],
                "other_physical_features": [
                    "heated body (you illuminate a 5ft radius with bright light and an additional 5ft with dim light)"
                ]
            }
        },
        "Water": {
            "ability_scores": {
                "wisdom": +1
            },
            "core_combat": {
                "speed_bonus": {"swimming": 30}
            },
            "other_info": {
                "resistances": ["cold"],
                "add_advantage_on": ["stealth (if underwater)"],
                "other_physical_features": [
                    "amphibious (air and water breathing)",
                    ("darkvision", 60, "ft")
                ]
            }
        },
        "Flying Mantis": {
            "core_combat": {
                "speed_bonus": {"flying": 20}
            },
            "ability_scores": {
                "strength": +1
            },
            "other_info": {
                "other_physical_features": [
                    "acid production (natural acid secretion)",
                    "sharp forelimbs (1d6 slashing damage)"
                ]
            }
        },
        "Hornet": {
            "core_combat": {
                "speed_bonus": {"flying": 30}
            },
            "ability_scores": {
                "constitution": +1
            },
            "other_info": {
                "other_physical_features": [
                    "honey production",
                    "natural stinger (1d4 piercing + poison)"
                ]
            }
        },
        "Bumblebee": {
            "core_combat": {
                "speed_bonus": {"flying": 25}
            },
            "ability_scores": {
                "constitution": +2
            },
            "other_info": {
                "other_physical_features": [
                    "honey production",
                    "robust build (resistance to bludgeoning damage)"
                ]
            }
        },
        "Fly": {
            "core_combat": {
                "speed_bonus": {"flying": 35},
                "size": "small"
            },
            "ability_scores": {
                "dexterity": +1
            },
            "other_info": {
                "other_physical_features": [
                    "erratic flight (advantage on dexterity saves vs effects)"
                ]
            }
        },
        "Cockroacher": {
            "ability_scores": {
                "constitution": +2
            },
            "other_info": {
                "resistances": ["poison"],
                "other_physical_features": [
                    "limited flight (can glide up to 20ft)",
                    "extreme survivability (once per long rest, can drop to 0 hp and stabilize automatically)"
                ]
            }
        },
        "Antsyote": {
            "core_combat": {
                "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}, {"const": 2}]}
            },
            "ability_scores": {
                "strength": +2
            },
            "other_info": {
                "other_physical_features": [
                    "hive coordination (advantage on checks when allies are nearby)"
                ]
            }
        },
        "Ladybudger": {
            "core_combat": {
                "speed_bonus": {"flying": 20}
            },
            "ability_scores": {
                "constitution": +1,
                "wisdom": +1
            },
            "other_info": {
                "resistances": ["poison"],
                "other_physical_features": [
                    "aposematic coloration (bright warning colors)",
                    "defensive secretions (creatures that grapple you have disadvantage on ability checks)",
                    "fortune symbol (once per day, you can reroll a failed saving throw for yourself or an ally within 10ft)"
                ]
            }
        },
        "Mothyel": {
            "core_combat": {
                "speed_bonus": {"flying": 35}
            },
            "ability_scores": {
                "dexterity": +1,
                "charisma": +1
            },
            "other_info": {
                "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
                "other_physical_features": [
                    "nocturnal affinity (advantage on perception checks in dim light or darkness relying on sight)",
                    "powdered wings (can shed scales to escape grapples once per short rest)"
                ]
            }
        },
        "Bebeesner": {
            "ability_scores": {
                "dexterity": +2
            },
            "core_combat": {
                "speed_bonus": {"walking": 5, "climbing": 25},
                "size": "small"
            }
        },
        "Dawg": {
            "ability_scores": {
                "strength": +1,
                "charisma": +1
            },
            "proficiencies": {
                "skills": ["athletics"]
            },
            "other_info": {
                "other_physical_features": [
                    "canine loyalty (advantage on saving throws against being frightened when an ally is within 5ft)",
                    "playful demeanor (advantage on charisma checks when interacting with children and animals)",
                    "keen smell (advantage on perception checks that rely on smell)"
                ]
            }
        },
        "Crimson Devil": {
            "ability_scores": {
                "strength": +1,
                "charisma": +2
            },
            "proficiencies": {
                "skills": ["intimidation"]
            },
            "other_info": {
                "add_advantage_on": ["death effects"],
                "other_physical_features": [
                    "small horns (1d4 piercing damage, light, versatile)"
                ]
            }
        },
        "Light Blue Devil": {
            "ability_scores": {
                "wisdom": +2,
                "charisma": +1
            },
            "proficiencies": {
                "skills": ["insight"]
            },
            "other_info": {
                "add_advantage_on": ["death effects"],
                "other_physical_features": [
                    "small horns (1d4 piercing damage, light, versatile)"
                ]
            }
        },
        "Jaguarfolk": {
            "ability_scores": {
                "strength": +2,
                "dexterity": +1
            },
            "core_combat": {
                "speed_bonus": {"walking": 5, "climbing": 30, "swimming": 25}
            },
            "other_info": {
                "other_physical_features": [
                    "powerful build (carries/pushes as one size larger)",
                    "predatory instincts (advantage on perception and survival checks related to hunting/tracking)",
                    "silent movement"
                ]
            }
        },
        "Onicronimb": {
            "ability_scores": {
                "dexterity": +2,
                "constitution": +1
            },
            "other_info": {
                "resistances": ["cold", "fire"],
                "other_physical_features": [
                    "jumping spider heritage (can jump up to 30ft horizontally and 15ft vertically)",
                    "wall-climbing (can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check)"
                ]
            }
        },
        "Octolen": {
            "ability_scores": {
                "constitution": +2,
                "intelligence": +1
            },
            "other_info": {
                "other_physical_features": [
                    "tentacled lower body (can use tentacles for manipulation and movement)",
                    "amphibious (breaths air and water)",
                    "ink secretion (can release ink to obscure vision in a 10ft radius once per short rest)"
                ]
            }
        },
        "Browish": {
            "core_combat": {
                "ac": +2,
                "size": "large"
            },
            "ability_scores": {
                "strength": +2,
                "constitution": +1
            },
            "other_info": {
                "resistances": ["cold"]
            }
        },
        "Skullywag": {
            "ability_scores": {
                "dexterity": +1,
                "charisma": +1
            },
            "proficiencies": {
                "skills": ["performance", "sleight of hand"],
                "tools": ["disguise kit"],
                "armors": ["light"]
            }
        },
        "Other": {
            "ability_scores": {
                "constitution": +1
            },
            "proficiencies": {
                "weapons": ["random_weapon_list"],
                "skills": ["random_skill_list"]
            }
        }
    }

#ToDo
age_category = {
        "child": {
        "core_combat": {
                "speed_bonus": {"walking": -5,
                                "flying": -5,
                                "swimming": 0,
                                "climbing": -10
                                }, #it's going to be added to the computed speeds
                "size": "" #basic is medium
            },
            "ability_scores": {
                "strength": 0,
                "dexterity": 2,
                "constitution": 0,
                "intelligence": 1,
                "wisdom": 0,
                "charisma": 0
            },
            "proficiencies": {
                "weapons": ["longsword","shortsword","longbow","shortbow"],
                "armors": [],
                "tools": [],
                "skills": ["perception"],
                "saving_throws": []
            },
            "magic": {
                "magic_source": "Innate",
                "spellcasting_ability": "",
                "spell_slots": {1: 0, 2: 0},
                "known_spells": [],
                "known_cantrips": ["wizard_cantrip_list"]
            },
            "other_info": {
                "resistances": [],
                "immunities": ["charmed (magic-induced sleep)"],
                "vulnerabilities": [],
                "add_advantage_on": [],
                "add_disadvantage_on": [],
                "other_physical_features": [("darkvision", 60, "ft")]
            }
        },
        "teen": {"wisdom": +2, "speed": -5},
        "adult": {"dexterity": +2},
        "middle-aged": {"dexterity": +2},
        "elderly": {"dexterity": +2}
    }

#ToDo
occupation = {
        "Farmer/Field Worker": {"dexterity": +2},
        "Unemployed": {"dexterity": +2}
    }

#ToDo
backstory_seed = {
        "Runaway noble child": {"dexterity": +2},
        "Former slave": {"dexterity": +2}
    }

#ToDo
wealth = {
        "Royal": {"dexterity": +2},
        "Noble": {"dexterity": +2},
        "Commoner": {"dexterity": +2},
        "Peasant": {"dexterity": +2},
        "Slave": {"dexterity": +2}
    }       

