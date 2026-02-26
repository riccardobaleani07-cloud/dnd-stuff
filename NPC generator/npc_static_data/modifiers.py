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
# Notes on list for post format: random_weapon_list, plantfolk_vulnerability_list, random_toolkit_list, random_damage_type_list, lycantrope_natural_weapons_list, aasimar_transformation_list, random_skill_list, giant_element_list, draconic_ancestory_list, musical_instrument_list, wizard_cantrip_list, druid_cantrip_list, martial_weapon_list, simple_weapon_list
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
musical_instrument_list = []
random_first_level_spell = []
cleric_cantrip_list = []
giant_element_list = []
draconic_ancestory_list = [] # (ex: red dragon (fire type))
plantfolk_vulnerability_list = []
aasimar_transformation_list = [] # (ex: transformation name (description))
lycantrope_natural_weapons_list = [] # (ex: natural weapons (bite, 1d6 piercing damage))



race = { # Common elf contains the complete template
    "Common Elf": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"const": 0}]},
            "ac": {"apply": "add", "expr": [{"const": 0}]},
            "initiative": {"apply": "add", "expr": [{"const": 0}]},
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 0}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
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
            "spell_slots": {"spell_slots.1": {"apply": "add", "expr": [{"const": 0}]},
                            "spell_slots.2": {"apply": "add", "expr": [{"const": 0}]}},
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
            "speed_bonus": {"speed.walking": 
                                {"apply": "add", "expr": [{"const": 5}]}
                            }, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
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
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]},
                            "speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
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
            "tools": {"apply": "add", "expr": [{"rd_choice": random_toolkit_list}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"rd_choice": [ArmorType.UNARMORED, ArmorType.LIGHT, ArmorType.MEDIUM, ArmorType.HEAVY]}, {"stat": "armors"}]}]},
            "saving_throws": {"apply": "add", "expr": [{"rd_choice": ["dexterity", "strenght", "constitution", "wisdom", "charisma", "intelligence"]}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"rd_choice": [MagicSource.INNATE, MagicSource.NONE]}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"rd_choice": ["wisdom", "intelligence", "charisma"]}]},
            "spell_slots": {"spell_slots.1": {"apply": "add", "expr": [{"rd_choice": [0, 0, 0, 1, 1, 2]}]},
                            "spell_slots.2": {"apply": "add", "expr": [{"rd_choice": [0, 0, 1]}]}},
            "known_spells": {"apply": "add", "expr": [{"rd_choice": random_first_level_spell}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": {"add": [wizard_cantrip_list, druid_cantrip_list, cleric_cantrip_list]}}]}
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
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}
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
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
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
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}},
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
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"add": [{"const": 10}, {"stat": "speed.walking"}]}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
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
    "Sylph": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}} #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "acrobatics"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "wisdom"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "gust of wind (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "gust"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["thunder", "lightning"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "slow fall (reduce fall damage by 20ft)"}]}
        }
    },
    "Dryad": {
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["club","quarterstaff","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["nature","survival"]}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "wisdom"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "entangle (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "druidcraft"}]}
        }
    },
    "Gnome": {
        "core_combat": {
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": "tinker's tools"}]},
            "skills": {"apply": "add", "expr": [{"const": "history"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "intelligence"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "detect magic (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "minor illusion"}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Dwarf": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": -5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["battleaxe","warhammer","handaxe","shield"]}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.MEDIUM}, {"stat": "armor_type"}]}]},
            "tools": {"apply": "add", "expr": [{"const": ["smith's tools","brewer's supplies","mason's tools"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Tabaxi": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 10}]},
                            "speed.climbing": {"apply": "replace", "expr": [{"const": 40}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": "claws"}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception","stealth"]}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "charmed (magic-induced sleep)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["feline agility (free dash 1/rest)", ("darkvision", 60, "ft"),
                                        "cat's claws (natural weapons, 1d4 slashing damage)"]}]}
        }
    },
    "Kenku": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": ["forgery kit", "disguise kit"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["stealth", "sleight of hand"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "mimicry"]}]}
        }
    },
    "Goliath": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"multiply": [{"const": 3}, {"stat": "level"}]}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": simple_weapon_list}, {"rd_choice": random_weapon_list}, {"const": "shield"}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.MEDIUM}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": "athletics"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "cold"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "stone's endurance (free stone skin 1/rest)"}]}
        }
    },
    "Beastfolk": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": "enhanced senses (advantage on perception checks involving smell, sight, or hearing)"}]}
        }
    },
    "Satyr": {
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": "horns"}]},
            "tools": {"apply": "add", "expr": [{"rd_choice": musical_instrument_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["performance","persuasion"]}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "charm person (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "minor illusion"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": "horns (natural weapons, 1d4 bludgeoning damage)"}]}
        }
    },
    "Bugbear": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": -1}]},
            "charisma": {"apply": "add", "expr": [{"const": -1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": ["intimidation", "stealth"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": ["long-limbed (reach increased by 5ft)",
                                        "sneaky (advantage on stealth checks in dim light or darkness)"]}]}
        }
    },
    "Sentient Construct": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 2}]},
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": -1}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": "artisan's tools"}]},
            "skills": {"apply": "add", "expr": [{"const": "arcana"}]},
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "add", "expr": [{"const": "intelligence"}]},
            "spell_slots": {"spell_slots.1": 2,
                            "spell_slots.2": 1},
            "known_spells": {"apply": "add", "expr": [{"const": ["mage armor", "shield"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["mending", "mage hand"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
            "immunities": {"apply": "add", "expr": [{"const": "diseased"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "cold"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["does not need to eat, drink, breathe, or sleep", "can concentrate on spells even while incapacitated"]}]}
        }
    },
    "Giant": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.LARGE}]}, #basic is medium
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 3}]},
            "dexterity": {"apply": "add", "expr": [{"const": -1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}, {"rd_choice": simple_weapon_list}]},
            "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.MEDIUM}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": "athletics"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"rd_choice": giant_element_list}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "enlarged reach (reach increased by 5ft)"}]}
        }
    },
    "Wolfang": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["claws","bite"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception", "survival"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "diseases"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "keen hearing", "keen smell",
                                        "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)",
                                        "natural weapons (claws 1d4 slashing damage, bite 1d6 piercing damage)"]}]}
        }
    },
    "Dragonborn": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}, {"rd_choice": simple_weapon_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"rd_choice": draconic_ancestory_list}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["breath weapon (15ft cone or 30ft line, 2d6 damage (same type as the ancestory type), DC 12 dex save for half)",
                                                                {"rd_choice": draconic_ancestory_list}]}]}
        }
    },
    "Half-Dragon": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 2}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 40}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": "bite"}]},
            "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"rd_choice": draconic_ancestory_list}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["breath weapon (15ft cone or 30ft line, 2d6 damage (same type as the ancestory type), DC 12 dex save for half)",
                                        "natural weapons (bite 1d8 piercing damage)",
                                        {"rd_choice": draconic_ancestory_list}]}]}
        }
    },
    "True Dragon": {
        "core_combat": {
            "hp": {"apply": "multiply", "expr": [{"const": 3}]},
            "ac": {"apply": "add", "expr": [{"const": 4}]},
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 10}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["breath weapon","claws","bite"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["intimidation","perception"]}]}
        },
        "magic": {
            "magic_source": {"apply": "replace", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["fear (free 1/day)", "telepathy (at will)"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "diseases"}]},
            "immunities": {"apply": "add", "expr": [{"rd_choice": draconic_ancestory_list}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 120, "ft"),
                                        "breath weapon (30ft cone or 60ft line, 4d6 damage (same type as the ancestory), DC 15 dex save for half)",
                                        "trasformation (can polymorph into dragonish (and back) form gaining flight 60ft, the huge size, natural weapons (bite 2d10 piercing damage, claw 2d6 slashing damage))",
                                        "legendary resistance (3/rest, can choose to succeed a failed saving throw)",
                                        {"rd_choice": draconic_ancestory_list}]}]}
        }
    },
    "Kobold": {
        "core_combat": {
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}, #basic is medium
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger","sling","shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"rd_choice": random_skill_list}]}
        },
        "other_info": {
            "vulnerabilities": {"apply": "add", "expr": [{"const": "sunlight sensitivity"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"),
                                        "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)"]}]}
        }
    },
    "Lizardfolk": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 1}]},
            "speed_bonus": {"speed.swimming": {"apply": "replace", "expr": [{"const": 30}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["bite","club","javelin","spear"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["survival","perception"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("hold breath", 15, "minutes"), "natural weapons (bite 1d6 piercing damage)"]}]}
        }
    },
    "Firefly": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 10}]},
                            "speed.flying": {"apply": "replace", "expr": [{"const": 40}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.TINY}]}, #basic is medium
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": "sting"}]},
            "skills": {"apply": "add", "expr": [{"const": "stealth"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "produce flame (free at will)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "faerie fire"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "cold"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "bioluminescence (can emit bright light in 10ft radius and dim light for additional 10ft)"]}]}
        }
    },
    "Pale Knight": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]},
            "initiative": {"apply": "divide", "expr": [{"stat": "dexterity_mod"}]},
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 10}]}},  # 20 ft base
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": -1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "rapier"]}]},
            "tools": {"apply": "add", "expr": [{"const": "masons tools"}]},
            "skills": ["perception", "deception"]
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": druid_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["necrotic", "poison"]}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "petrified"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "blind (cannot see normally)",
                ("telepathy (other Paladrins only)", 60, "ft"),
                ("thermal vision", 10, "ft"),
                "dark sustenance (does not need to eat or drink normally)",
                "mute (doesn't speak normally)"
            ]}]}
        }
    },
    "Lost Goblin": {
        "core_combat": {
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}, #basic is medium
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["shortsword", "shortbow"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["insight","intimidation"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "nimble escape (can take disengage or hide action as a bonus action on each of its turns)"]}]}
        }
    },
    "Hobgoblin": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["history","intimidation"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "martial advantage (when it or an ally within 5ft attacks with a martial weapon, can roll with advantage)"]}]}
        }
    },
    "Lost Sea Goblin": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]},
                            "speed.swimming": {"apply": "replace", "expr": [{"const": 40}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
            "size": {"apply": "add", "expr": [{"const": Size.SMALL}]}, #basic is medium
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["trident", {"rd_choice": random_weapon_list}]}]},
            "skills": {"apply": "add", "expr": [{"const": ["athletics", "insight"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "wisdom"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "minor illusion (free 4/day)"}]}
            },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), ("hold breath", 30, "minutes")]}]}
        }
    },
    "Mushroomfolk": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}, #basic is medium
        },
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": "unarmed strike"}]},
            "skills": {"apply": "add", "expr": [{"const": ["nature", "medicine"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "add", "expr": [{"const": "wisdom"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "fungal spores (free 2/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": druid_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "keen smell"}]}
        }
    },
    "Ogre": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 2}]},
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 10}]}}, #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
            "size": {"apply": "replace", "expr": [{"const": Size.LARGE}]}, #basic is medium
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["unarmed strike", "greatclub"]}]},
            "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                        "fists of steel (natural weapons, 1d8 bluedgeoning damage)"]}]}
        }
    },
    "Half-Ogre": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["unarmed strike", "greatclub"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["intimidation", "athletics"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                        "heavy fists (natural weapons, 1d6 bluedgeoning damage)"]}]}
        }
    },
    "Insectoid": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 3}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                ("electroreception (sense electrical fields)", 30, "ft"),
                "compound eyes or mandibles",
                "insectoid physiology"
            ]}]}
        }
    },
    "Grung": {
        "core_combat": {
            "speed_bonus": {"speed.climbing": {"apply": "replace", "expr": [{"const": 25}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "athletics"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "poisoned"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "amphibious (can breathe air and water)",
                "poisonous skin (contact poison, DC 12 con save or be poisoned for 1 min)",
                "standing leap (long jump 25ft, high jump 15ft without run-up)"
            ]}]}
        }
    },
    "Kling": {
        "core_combat": {
            "speed_bonus": {"speed.swimming": {"apply": "replace", "expr": [{"const": 20}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": "tinkers tools"}]},
            "skills": {"apply": "add", "expr": [{"const": ["sleight_of_hand", "survival"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                "amphibious (can breathe air and water)",
                "scavenger culture (advantage on checks to find usable materials)"
            ]}]}
        }
    },
    "Halfling": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}},
            "size": {"apply": "add", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "stealth"}]}
        },
        "other_info": {
            "add_advantage_on": {"apply": "add", "expr": [{"const": "frightened"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ["lucky (reroll a nat 1 on a d20)",
                                                                            "nimbleness (you can move through a creature bigger than you)"]}]}
        }
    },
    "Orc": {
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["greataxe", "javelin"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"),
                                                                            "powerful build (counts as one size larger for carrying capacity and push/drag/lift"]}]}
        }
    },
    "Plantfolk": {
        "core_combat": {
            "speed_bonus": {"speed.climbing": {"apply": "replace", "expr": [{"const": 10}]}}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]},
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "quarterstaff", "sickle"]}]},
            "tools": {"apply": "add", "expr": [{"const": ["herbalism kit", "alchemist supplies"]}]},
            "skills": {"apply": "add", "expr": [{"const": ["nature", "perception", "survival"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["entangle (free at will)", "goodberry (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "druidcraft"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"rd_choice": plantfolk_vulnerability_list}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": ["nature", "herbalism kit", "prone", "stealth (in foliage)"]}]}
        }
    },
    "Tiefling": {
        "ability_scores": {
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "thaumaturgy"}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["disguise self (free 1/day)", "hellish rebuke (free 1/day)"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Demonoid": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 15}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "longsword", "shortsword"]}, {"rd_choice": exotic_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["intimidation", "arcana"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": "hellish rebuke (free 1/day)"}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "thaumaturgy"}, {"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "demonic heritage (can recall demonic powers, manifests as luminescent horns, wings or tail)",
                ("darkvision", 60, "ft")
            ]}]}
        },
    },
    "Yuan-Ti": {
        "ability_scores": {
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "poison spray"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "suggestion (free 1/day)"}]}
        },
        "other_info": {
            "immunities": {"apply": "add", "expr": [{"const": "poison"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"), "magic resistance (advantage vs spells that force a saving throw)"]}]}
        }
    },
    "Demon": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"op": "multiply", "value": [{"stat": "proficiency_bonus"}, {"stat": "level"}]}]},
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "longsword", "shortsword"]}, {"rd_choice": exotic_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["intimidation", "arcana"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["darkness (free 1/day)", "teleport (free 1/day)", "hellish rebuke (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["thaumaturgy", "wizard_cantrip_list", "message"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["fire", "cold", "lightning", "force"]}]},
            "immunities": {"apply": "add", "expr": [{"const": ["charmed", "frightened"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": ["radiant", "necrotic"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 120, "ft"),
                                        "regeneration (regain 5 HP at the start of its turn if it has at least 1 HP)",
                                        "demonic taunt (once per turn, can deal extra 7 (2d6) necrotic damage to a creature it hits with a weapon attack)",
                                        ("true sight", 45, "ft")]}]}
        }
    },
    "Salamanderman": {
        "core_combat": {
            "speed_bonus": {"speed.swimming": {"apply": "replace", "expr": [{"const": 20}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "shortsword"]}, {"rd_choice": simple_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["survival", "nature"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "athletics (when balance is needed)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "regenerative skin (heals minor wounds faster for 1d4 HP at the start of its turn)",
                "tail can be used for balance or minor attacks (1d4 bludgeoning)",
                ("darkvision", 60, "ft")
            ]}]}
        }
    },
    "Oni": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword", "katana", "shortsword"]}, {"rd_choice": martial_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "fire bolt"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                "horns (natural weapons, 1d6 piercing damage)",
                "innate flame affinity (fire generate by your spells is deep red or purple)"
            ]}]}
        }
    },
    "Kijin": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}, {"const": 2}]},
            "size": {"apply": "replace", "expr": [{"const": Size.MEDIUM}]}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["longsword", "katana", "longbow"]}, {"rd_choice": martial_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "arcana"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["mage armor (free at will)", "detect magic (free at will)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                "magic vision (can see magic energy and auras)",
                "innate fire affinity (fire created by your spells is a colour of your choice)"
            ]}]}
        }
    },
    "Majin": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "dexterity_mod"}, {"const": 5}]},
            "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["perception", "intimidation"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["mage armor (free at will)", "detect magic (free at will)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}, {"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["fire", "necrotic"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                ("thermal vision", 10, "ft"),
                ("tremorsense", 10, "ft"),
                "heightened senses (advantage on perception checks involving smell, sight, or hearing)",
                "overwhelming presence (once per day, force all creatures within 30ft that can see you to make a DC 15 wisdom saving throw or be frightened for 1 minute)"
            ]}]}
        }
    },
    "Strix": {
        "ability_scores": {
            "intelligence": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": -1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["insight", "arcana"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "psychic"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": ["charmed", "frightened"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "tentacle manifestation (can grow/absorb grown tentacles from the back)",
                "grown tentacles can manipulate objects but cannot wield weapons",
                "self-replication capable (rare, slow process)"
            ]}]}
        }
    },
    "Nightmare": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["deception", "insight"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "spell_slots": {"spell_slots.1": 2,
                            "spell_slots.2": 2},
            "known_spells": {"apply": "add", "expr": [{"const": ["sleep (free 1/day)", "cause fear (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["minor illusion", "friendship"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "psychic"}]},
            "immunities": {"apply": "add", "expr": [{"const": "magical sleep"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "feared"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "shapeshifter (humanoid forms only, still a shadowy halo remains)",
                "nightmare induction (creatures that sleep within 30ft may suffer disturbing dreams and not gain benefits of a long rest at your discrection)",
                "dream-feeding (regain 2d6 hp after inducing a nightmare)"
            ]}]}
        }
    },
    "Celestial": {
        "core_combat": {
            "initiative": {"apply": "add", "expr": [{"stat": "wisdom_mod"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 15}]}}
        },
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"rd_choice": simple_weapon_list}, {"rdChoice", martial_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "insight"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["cure wounds (free 3/day)", "protection from evil and good (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["thaumaturgy", "light"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "radiant"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "feared"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "celestial heritage (can manifest wings of light, halo and/or radiant tail)",
                ("darkvision", 60, "ft"),
                ("true sight", 30, "ft")
            ]}]}
        }
    },
    "Angel": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"op": "multiply", "value": [{"stat": "proficiency_bonus"}, {"stat": "level"}]}]},
            "ac": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["spear", "longsword", "longbow"]}, {"rd_choice": random_weapon_list}]},
            "armors": {"apply": "add", "expr": [{"max": [{"const": ArmorType.HEAVY}, {"stat": "armors"}]}]},
            "skills": {"apply": "add", "expr": [{"const": ["insight", "arcana"]}]},
            "saving_throws": {"apply": "add", "expr": [{"const": ["wisdom", "charisma"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["shield of faith (free at will)", "lesser restoration (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["light", "thaumaturgy"]}, {"rd_choice": cleric_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["radiant", "necrotic"]}]},
            "immunities": {"apply": "add", "expr": [{"const": ["charmed", "frightened"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": ["fire", "cold", "lightning", "force"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "divine regeneration (regain 5 hp at the start of its turn if it has at least 1 hp)",
                "angelic touch (heals a creature or mends an object for 2d4 + 3 hp as an action, on touch)",
                ("darkvision", 120, "ft"),
                ("true sight", 30, "ft")
            ]}]}
        }
    },
    "Aarakocra": {
        "core_combat": {
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 50}]}} #it's going to be added to the base speed (speed.walking is 30ft others are 0) of the specified type
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": ["keen sight (advantage on perception checks that rely on sight)", "talons (natural weapons, 1d4 slashing)"]}]}
        }
    },
    "Aasimar": {
        "ability_scores": {
            "charisma": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "light"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["radiant", "necrotic"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                {"rd_choice": aasimar_transformation_list}
            ]}]}
        }
    },
    "Moonling": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["survival", "perception"]}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "light-perception vision (cannot see shapes or colors, only light intensity; blinded by magical darkness)",
                ("tremorsense", 30, "ft"),
                ("magnetosense", 60, "ft"),
                "keen hunter (advantage on survival checks to track creatures)",
                "generational grudge (once a Moonling has been harmed by a creature, that creature has disadvantage on charisma checks against Moonlings of the same community)"
            ]}]}
        }
    },
    "Foxling": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["heavy crossbow", "spear", "hand fans"]}, {"rd_choice": random_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": ["stealth", "insight"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "minor illusion"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": [("darkvision", 60, "ft"),
                "fox senses (recognizes individuals by scent and magical trace: has advantage on uncovering true identity)",
                ("termic vision (can detect warm creatures)", 15, "ft"),
                "natural agility (advantage on dexterity saving throws against effects you can see)"
            ]}]}
        }
    },
    "Shadowkin": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 4}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "armors": {"apply": "add", "expr": [{"max": [{"const": ArmorType.HEAVY}, {"stat": "armor"}]}]},
            "weapons": {"apply": "add", "expr": [{"const": "shield"}, {"rd_choice": simple_weapon_list}, {"rd_choice": random_weapon_list}]},
            "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "necrotic"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "frightened"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                "armor shell (can inhabit incomplete or abandoned armor that drops if defeated)"
            ]}]}
        }
    },
    "Wisp": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": +5}]},
            "initiative": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.TINY}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": -1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["arcana", "stealth"]}]},
            "saving_throws": {"apply": "add", "expr": [{"const": ["dexterity", "wisdom"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "charisma"}]},
            "spell_slots": {"spell_slots.1": 2},
            "known_spells": {"apply": "add", "expr": [{"const": ["light (free 1/day)", "mage hand (free 2/day)", "minor illusion (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["lightning", "poison"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"]}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "stealth (in dim light or darkness)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "incorporeal form (can pass through small openings, 1 inch wide, cannot wear armor or carry objects)",
                "glowing body (light radius 10ft, can dim at will)",
                "possessive ability (can attempt to possess a willing or incontious humanoid once per short rest, duration 1 minute)",
                "hovering flight (hovers and flyes)"
            ]}]}
        }
    },
    "Voidling": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}},
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["dagger", "rapier"]}, {"rd_choice": simple_weapon_list}]},
            "tools": {"apply": "add", "expr": [{"const": ["tinkers tools", "jewelers tools"]}]},
            "skills": {"apply": "add", "expr": [{"const": "stealth"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"rd_choice": wizard_cantrip_list}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "necrotic"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 60, "ft"),
                ("telepathy (only in Voshedi)", 60, "ft"),
                "dark sustenance (does not need to eat or drink normally)",
                "darknesssynthesis (inverted photosynthesis)",
                "mute (doesn't speak normally)"
            ]}]}
        }
    },
    "Lycanthrope": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 2}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "perception"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": ["silvered weapons"]}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": ["perception (smell)"]}]},
            "other_physical_features": [
                "hybrid nightime transformation (can transform into hybrid form only at night; transformation is more severe the more the moon is visible)",
                {"rd_choice": lycantrope_natural_weapons_list}
            ]
        }
    },
    "Sentient Undead": {
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": -1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "history"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "necrotic"}]},
            "immunities": {"apply": "add", "expr": [{"const": ["poison", "disease"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "radiant"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "feared"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "charisma checks (dealing with the living)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "does not need food or air" }]}
        }
    },
    "Starborn": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
            "initiative": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 10}]},
                            "speed.flying": {"apply": "replace", "expr": [{"const": 20}]}},
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": -1}]},
            "intelligence": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 4}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["arcana", "history", "persuasion"]}]},
            "saving_throws": {"apply": "add", "expr": [{"const": ["intelligence", "charisma", "constitution"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "spellcasting_ability": {"apply": "replace", "expr": [{"const": "wisdom"}]},
            "spell_slots": {
                "spell_slots.1": {"apply": "add", "expr": [{"const": 4}]},
                "spell_slots.2": {"apply": "add", "expr": [{"const": 3}]},
                "spell_slots.3": {"apply": "add", "expr": [{"const": 3}]},
                "spell_slots.4": {"apply": "add", "expr": [{"const": 3}]},
                "spell_slots.5": {"apply": "add", "expr": [{"const": 3}]},
                "spell_slots.6": {"apply": "add", "expr": [{"const": 2}]},
                "spell_slots.7": {"apply": "add", "expr": [{"const": 2}]},
                "spell_slots.8": {"apply": "add", "expr": [{"const": 2}]},
                "spell_slots.9": {"apply": "add", "expr": [{"const": 2}]}
            },
            "known_spells": {"apply": "add", "expr": [{"const": ["wish", "meteor swarm", "plane shift", "disintegrate", "magic missle", "counterspell", "detect magic"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": ["light", "fire bolt"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["radiant", "force"]}]},
            "immunities": {"apply": "add", "expr": [{"const": ["diseased", "exhaustion (nonmagical)"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "psychic"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "stellar core (no need for air, food or sleep)",
                "energy dependency (at 16 spell slots or less, cannot fly and all the resistances are lost; at 5 spell slots or less gains mortal needs and looses immunity to exaustion effects; at 0 suffer from 1d8 + 2 damage for every half hour without sleep)",
                "slow recharge (regain spell slots only up to the 4th level after a long rest, plus 2 additional slot of the lowest level spent over 5th)",
                "half-familiar (you can bond with an other humanoid with a ritual: Stellar Covenant, 9th-level transmutation (ritual), Casting Time: 24 hours, Range: Touch, Components: V, S, M (a focus attuned to stellar energy worth at least 10,000 gp, consumed), Duration: Until broken, Description: this ritual forges a one-way metaphysical bond between a Starborn and a single willing creature, designating that creature as the Starborn's Chosen. In exchange of a predefined thing, the Chosen can order the Starborn to act. The pact can be broken by both if one is not fullfilling the pact's terms. The pact is exclusive.)",
                "bond-relyant caster (can cast spells above the 4th level only for a chosen bonded creature)",
                "restricted attunement (only one weapon (that act as focus) or focus of choice)",
                "fatigue sensitivity (disadvantage on constitution saving throws against exhaustion effects)",
                ("darkvision", 120, "ft"),
                ("termic vision", 30, "ft"),
                ("tremorsense", 30, "ft"),
                ("true sight", 15, "ft")
            ]}]}
        }
    },
    "Crystalborn": {
        "core_combat": {
            "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -2}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 2}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": "artisan tools"}]},
            "skills": {"apply": "add", "expr": [{"const": ["arcana", "perception"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "light"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "psychic"}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "thunder"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "arcana"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "stealth"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": ("darkvision", 60, "ft")}]}
        }
    },
    "Changeling": {
        "ability_scores": {
            "charisma": {"apply": "add", "expr": [{"const": 2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": "deception"}]}
        },
        "other_info": {
            "add_advantage_on": {"apply": "add", "expr": [{"const": "deception (related to identity manouvers)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": "shapechanger (humanoid appearance only)"}]}
        }
    },
    "True Vampire": {
        "core_combat": {
            "hp": {"apply": "add", "expr": [{"stat": "constitution_mod"}, {"stat": "proficiency_bonus"}]},
            "ac": {"apply": "add", "expr": [{"const": 1}]},
            "initiative": {"apply": "add", "expr": [{"stat": "charisma_mod"}]},
            "speed_bonus": {
                "speed.walking": {"apply": "add", "expr": [{"const": 5}]},
                "speed.flying": {"apply": "replace", "expr": [{"const": 30}]}
            }
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "tools": {"apply": "add", "expr": [{"const": "brewer supplies"}]},
            "skills": {"apply": "add", "expr": [{"const": ["perception", "persuasion"]}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "necrotic"}]},
            "immunities": {"apply": "add", "expr": [{"const": ["diseases", "poison", "exhaustion (non-magical)", "aging effects"]}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "death effects"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "perception (when garlic is in 10ft)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                ("darkvision", 120, "ft"),
                "enhanced senses (advantage on perception checks relying on smell, taste, or hearing)",
                "no heartbeat",
                "does not need to breathe",
                "regeneration (regain hit points equal to proficiency bonus at the start of turn if at least 1 HP and has consumed blood in the last 24 hours)",
                "phase step (can move through solid objects up to 10ft as difficult terrain)",
                "flight (hover; cannot wear heavy armor)",
                "mist form (once per short rest, transform into mist for 1 minute; cannot attack or cast spells, can pass through tiny openings, speed becomes flying 40ft)",
                "no reflection (mirrors and reflective surfaces do not show the creature)"
            ]}]}
        }
    },
    "Spectre": {
        "core_combat": {
            "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -2}]},
            "dexterity": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": -2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["perception", "stealth"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "thaumaturgy"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["necrotic", "psychic"]}]},
            "immunities": {"apply": "add", "expr": [{"const": ["poison", "diseased", "poisoned"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "radiant"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "stealth"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                ("darkvision", 60, "ft"),
                ("spectral sense (sense living creatures)", 60, "ft")
            ]}]}
        }
    },
    "Triton": {
        "core_combat": {
            "speed_bonus": {"speed.swimming": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": 1}]},
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["trident", "spear"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": "fog cloud (free 1/day)"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "cold"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "amphibious (breathe air and water)",
                "aquatic adaptation (water contact reveals scale skin, gills, webbed fingers/toes)",
                ("darkvision", 120, "ft")
            ]}]}
        }
    },
    "Mermaid": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "remove", "expr": [{"const": 20}]},
                            "speed.swimming": {"apply": "replace", "expr": [{"const": 45}]}}
        },
        "ability_scores": {
            "constitution": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "shape water"}]},
            "known_spells": {"apply": "add", "expr": [{"const": "water breathing (free at will)"}]}
        },
        "other_info": {
            "other_physical_features": {"apply": "add", "expr": [{"const": "amphibious (breath air and water)"}]}
        }
    },
    "Nymph": {
        "ability_scores": {
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 2}]}
        },
        "proficiencies": {
            "saving_throws": {"apply": "add", "expr": [{"const": "dexterity"}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["charm person (free 3/day)", "entangle (free at will)"]}]}
        },
        "other_info": {
            "add_advantage_on": {"apply": "add", "expr": [{"const": "charmed"}]}
        }
    },
    "Turtoid": {
        "core_combat": {
            "ac": {"apply": "add", "expr": [{"const": 1}]},
            "initiative": {"apply": "subtract", "expr": [{"stat": "dexterity_mod"}]},
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]},
                            "speed.swimming": {"apply": "replace", "expr": [{"const": 20}]}}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": -1}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]}
        },
        "proficiencies": {
            "weapons": {"apply": "add", "expr": [{"const": ["club", "spear"]}]},
            "skills": {"apply": "add", "expr": [{"const": "survival"}]},
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": "cold"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "strength (carrying or pushing)"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "dexterity saving throws"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "tough shell (can retract as a bonus action to increase AC by 3)",
                ("hold breath", 15, "minutes")
            ]}]}
        }
    },
    "Gooba": {
        "core_combat": {
            "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 10}]},
                            "speed.swimming": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "dexterity": {"apply": "add", "expr": [{"const": 2}]},
            "constitution": {"apply": "add", "expr": [{"const": 2}]},
            "intelligence": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": -1}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["stealth", "athletics"]}]}
        },
        "other_info": {
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"]}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "amphibious (can breathe air and water)",
                "dehydration weakness (after 24 hours without at least 2 hours submerged in water, gain one level of exhaustion per day)",
                "tentacular limbs (can interact with objects, grapple, or climb using tentacles; advantage on grapple checks)",
                "chromatic shift (using an action it can change skin color briefly to hide; gains advantage on the stealth check)",
                "ink burst (once per short rest, release ink in a 10ft radius underwater, heavily obscured for 1 minute)",
                ("darkvision", 60, "ft")
            ]}]}
        }
    },
    "Banshee": {
        "core_combat": {
            "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
        },
        "ability_scores": {
            "strength": {"apply": "add", "expr": [{"const": -1}]},
            "constitution": {"apply": "add", "expr": [{"const": -1}]},
            "wisdom": {"apply": "add", "expr": [{"const": 1}]},
            "charisma": {"apply": "add", "expr": [{"const": 3}]}
        },
        "proficiencies": {
            "skills": {"apply": "add", "expr": [{"const": ["intimidation", "performance"]}]}
        },
        "magic": {
            "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
            "known_spells": {"apply": "add", "expr": [{"const": ["fear (free 1/day)", "silent image (free 1/day)"]}]},
            "known_cantrips": {"apply": "add", "expr": [{"const": "vicious mockery"}]}
        },
        "other_info": {
            "resistances": {"apply": "add", "expr": [{"const": ["necrotic", "psychic"]}]},
            "immunities": {"apply": "add", "expr": [{"const": ["poison", "charmed", "poisoned", "frightened"]}]},
            "vulnerabilities": {"apply": "add", "expr": [{"const": "radiant"}]},
            "add_advantage_on": {"apply": "add", "expr": [{"const": "intimidation"}]},
            "add_disadvantage_on": {"apply": "add", "expr": [{"const": "concentration (for maintaining spells)"}]},
            "other_physical_features": {"apply": "add", "expr": [{"const": [
                "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                "wail resonance (once per long rest, emit a wail causing all creatures within 30ft to make a DC 15 constitution saving throw or take 4d6 psychic damage and be frightened for 1 minute; half damage and no fright on successful save)",
                ("darkvision", 60, "ft"),
                ("spectral sense (sense living creatures)", 60, "ft")
            ]}]}
        }
    }
}

subtype = {
        "Shell": {
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "force"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "shell recall (1/day, grant temporary protection for the next minute: any creature within 10ft suffer the effect of the spell Armor of Agathys at lvl 1, yourself included)"
                ]}]}
            }
        },
        "Lush": {
            "ability_scores": {
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "lush recall (1/day, restore vitality in area for the next minute: any object suffers from mending effect, and every creature heal for 1d6 hp if starts the turn within 10 ft from you, you included)"}]}
            }
        },
        "Grace": {
            "ability_scores": {
                "wisdom": {"apply": "add", "expr": [{"const": 1}]},
                "constitution": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "cold"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "frost aura (willingly standing still (it means: not using movement, actions (except for the dodge action), bonus actions or reactions), can freeze up surroundings, up to freezing water and brittle metal in a 5ft radius, every creature within range that starts the turn there, must make a constitution DC 12 or suffer 4d6 cold damage, half on a success; you also have to perform the saving throw, but taking half the damage on success and none on failure)"}]}
            }
        },
        "Ghost": {
            "core_combat": {
                "hp": {"apply": "subtract", "expr": [{"stat": "proficiency_bonus"}]},
                "initiative": {"apply": "add", "expr": [{"stat": "proficiency_bonus"}]},
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
            },
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": -3}]},
                "dexterity": {"apply": "add", "expr": [{"const": 2}]},
                "constitution": {"apply": "add", "expr": [{"const": -3}]},
                "intelligence": {"apply": "add", "expr": [{"const": 1}]},
                "wisdom": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": ["necrotic", "slashing (nonmagical)", "piercing (nonmagical)", "bludgeoning (nonmagical)"]}]},
                "vulnerabilities": {"apply": "add", "expr": [{"const": "radiant"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "incorporeal movement (can move through objects as if they're difficult terrain)",
                    "cannot wear armor"
                ]}]}
            }
        },
        "Skeleton": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": -1}]},
                "dexterity": {"apply": "add", "expr": [{"const": 2}]},
                "constitution": {"apply": "add", "expr": [{"const": -1}]},
                "charisma": {"apply": "add", "expr": [{"const": -1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "piercing"}]},
                "vulnerabilities": {"apply": "add", "expr": [{"const": "bludgeoning"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": "does not bleed"}]}
            }
        },
        "Zombie": {
            "core_combat": {
                "hp": {"apply": "add", "expr": [{"stat": "constitution_mod"}]},
                "initiative": {"apply": "subtract", "expr": [{"stat": "dexterity_mod"}]},
                "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 5}]}}
            },
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]},
                "dexterity": {"apply": "add", "expr": [{"const": -2}]},
                "constitution": {"apply": "add", "expr": [{"const": 2}]},
                "intelligence": {"apply": "add", "expr": [{"const": -1}]},
                "charisma": {"apply": "add", "expr": [{"const": -1}]}
            },
            "other_info": {
                "vulnerabilities": {"apply": "add", "expr": [{"const": "fire"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "relentless endurance (first time reduced to 0 hp, drop to 1 instead, once per long rest)"}]}
            }
        },
        "Cerberian": {
            "ability_scores": {"strength": {"apply": "add", "expr": [{"const": 1}]},
                               "constitution": {"apply": "add", "expr": [{"const": 1}]}},
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "heat aura (willingly standing still (it means: not using movement, actions (except for the dodge action), bonus actions or reactions), can warm surroundings, up to melting metal in a 5ft radius, every creature within range that starts the turn there, must make a dexterity DC 14 or suffer 4d6 fire damage, half on a success; you also have to perform the saving throw, but taking half the damage on success and none on failure)"}]}
            }
        },
        "Blood Beat": {
            "ability_scores": {"charisma": {"apply": "add", "expr": [{"const": 2}]}},
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "blood manipulation (can control blood in a small area, up to 15ft radius)"}]}
            }
        },
        "Wither": {
            "ability_scores": {"wisdom": {"apply": "add", "expr": [{"const": 1}]},
                               "constitution": {"apply": "add", "expr": [{"const": 1}]}},
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "life drain (1/day, can recall powers to drain life in a area of 10ft radius for one minute: any creature that starts its turn there takes 1d6 necrotic damage and you heal for that amount for each creature in the area)"}]}
            }
        },
        "Steam": {
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 1}]},
                "wisdom": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
                "add_advantage_on": {"apply": "add", "expr": [{"const": "concentration (for maintaining spells)"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "obscuring mist (can lightly obscure a 10ft radius sqare within 60ft once per short rest)"}]}
            }
        },
        "Dust": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 2}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "dust cloud body (can impose disadvantage on one ranged (nonmagical) attack against you per turn before after seeing the dice result)"}]}
            }
        },
        "Smoke": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "fire"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "smoky form (can obscure a 5ft radius around self, once per long rest)",
                    "choking presence (creatures adjacent have disadvantage on perception checks relying on sight)"]}]}
            }
        },
        "Lava": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "core_combat": {
                "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "fire"}]}
            }
        },
        "Ice": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "immunities": {"apply": "add", "expr": [{"const": "cold"}]},
                "vulnerabilities": {"apply": "add", "expr": [{"const": "fire"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "frozen skin (you can choose that creature that touch you take 2d6 cold damage as a reaction)"}]}
            }
        },
        "Mud": {
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 1}]},
                "strength": {"apply": "add", "expr": [{"const": 1}]}
            },
            "core_combat": {
                "speed_bonus": {"speed.walking": {"apply": "subtract", "expr": [{"const": 10}]}}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": ["poison", "bluedgeoning (nonmagical)"]}]},
                "add_advantage_on": {"apply": "add", "expr": [{"const": ["poisoned", "prone"]}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "difficult terrain affinity (ignores non-magical difficult terrain)"}]}
            }
        },
        "Earth": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": ["animal handling", "nature"]}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    ("tremorsense", 15, "ft"),
                    ("magnetosense", 60, "ft"),
                    ("electroreception (sense electrical fields)", 30, "ft")]}]}
            }
        },
        "Wind": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 1}]}
            },
            "core_combat": {
                "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "force"}]},
                "vulnerabilities": {"apply": "add", "expr": [{"const": "slashing"}]},
                "other_physical_features": [
                    "flickering form (disadvantage on opportunity attacks against you)",
                    "lightweight body (can hover 10ft off the ground)"
                ]
            }
        },
        "Fire": {
            "ability_scores": {
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "magic": {
                "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
                "known_spells": {"apply": "add", "expr": [{"const": ["heat metal (free 1/day)"]}]},
            },
            "other_info": {
                "immunities": {"apply": "add", "expr": [{"const": "fire"}]},
                "vulnerabilities": {"apply": "add", "expr": [{"const": "cold"}]},
                "other_physical_features": [
                    "heated body (you illuminate a 5ft radius with bright light and an additional 5ft with dim light)"
                ]
            }
        },
        "Water": {
            "ability_scores": {
                "wisdom": {"apply": "add", "expr": [{"const": 1}]}
            },
            "core_combat": {
                "speed_bonus": {"speed.swimming": {"apply": "replace", "expr": [{"const": 30}]}}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "cold"}]},
                "add_advantage_on": {"apply": "add", "expr": [{"const": "stealth (if underwater)"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "amphibious (air and water breathing)",
                    ("darkvision", 60, "ft")]}]}
            }
        },
        "Flying Mantis": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 20}]}}
            },
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "acid factory (natural acid secretion, 1d6 acid damage if someone touches it, cannot be spitted)",
                    "natural weapons (sharp forelimbs, 1d6 slashing damage)"]}]}
            }
        },
        "Hornet": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 30}]}}
            },
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "honey production (can produce 2 silver worth of honey per day; more of it makes you suffer 1 exhaustion level for each silver of honey you produce)",
                    "natural stinger (1d4 piercing + poisoned effect (con saving throw DC 14))",
                    ("electroreception (sense electrical fields)", 15, "ft")]}]}
            }
        },
        "Bumblebee": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 25}]}}
            },
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 2}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "bludgeoning"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "honey production (can produce 2 silver worth of honey per day; more of it makes you suffer 1 exhaustion level for each silver of honey you produce)", 
                    "natural stinger (1d4 piercing + poisoned effect (con saving throw DC 14); after using it you immediately drop to 0 HP on a failed con saving throw DC 14)",
                    ("electroreception (sense electrical fields)", 15, "ft")
                ]}]}
            }
        },
        "Fly": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 35}]}},
                "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
            },
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 2}]}
            },
            "other_info": {
                "add_advantage_on": {"apply": "add", "expr": [{"const": 
                    "dexterity saving throws)"}]}
            }
        },
        "Cockroacher": {
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 2}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
                "add_advantage_on": {"apply": "add", "expr": [{"const": "death effects"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "glider master (can glide up to 20ft)",
                    "extreme survivability (once per long rest, when drops to 0 hp he can drop to 1 hp instead)"]}]}
            }
        },
        "Antsyote": {
            "core_combat": {
                "ac": {"apply": "add", "expr": [{"stat": "constitution_mod"}]}
            },
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 2}]}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "used to pact tacktics (advantage on ability checks when allies are in sight or in 10ft of distance)"}]}
            }
        },
        "Ladybudger": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "replace", "expr": [{"const": 20}]}}
            },
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 1}]},
                "wisdom": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "poison"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "aposematic coloration (bright warning colors)",
                    "defensive secretions (creatures that grapple you have disadvantage on ability checks)",
                    "fortune symbol (once per day, you can reroll a failed saving throw for yourself or an ally within 10ft)",
                    ("electrosense (can sense electric fields)", 30, "ft")]}]}
            }
        },
        "Mothyel": {
            "core_combat": {
                "speed_bonus": {"speed.flying": {"apply": "add", "expr": [{"const": 35}]}}
            },
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "add_disadvantage_on": {"apply": "add", "expr": [{"const": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"]}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "nocturnal affinity (advantage on perception checks in dim light or darkness relying on sight)",
                    "powdered wings (can use an action and shed scales to automatically escape grapples once per short rest)",
                    ("termic vision", 30, "ft")]}]}
            }
        },
        "Bebeesner": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 2}]}
            },
            "core_combat": {
                "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]}, "speed.climbing": {"apply": "replace", "expr": [{"const": 25}]}},
                "size": {"apply": "replace", "expr": [{"const": Size.SMALL}]}
            }
        },
        "Dawg": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": "athletics"}]}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "canine loyalty (advantage on saving throws against being frightened when an ally is within 10ft)",
                    "playful demeanor (advantage on charisma checks when interacting with children and animals)",
                    "keen smell (advantage on perception checks that rely on smell)"
                ]}]}
            }
        },
        "Crimson Devil": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 2}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": "intimidation"}]}
            },
            "other_info": {
                "add_advantage_on": {"apply": "add", "expr": [{"const": "death effects"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "natural weapons (small horns, 1d4 piercing damage, light, versatile)"
                }]}
            }
        },
        "Light Blue Devil": {
            "ability_scores": {
                "wisdom": {"apply": "add", "expr": [{"const": 2}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": "insight"}]}
            },
            "other_info": {
                "add_advantage_on": {"apply": "add", "expr": [{"const": "death effects"}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": 
                    "natural weapons (small horns, 1d4 piercing damage, light, versatile)"}]}
            }
        },
        "Jaguarfolk": {
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 2}]},
                "dexterity": {"apply": "add", "expr": [{"const": 1}]}
            },
            "core_combat": {
                "speed_bonus": {"speed.walking": {"apply": "add", "expr": [{"const": 5}]},
                                "speed.climbing": {"apply": "replace", "expr": [{"const": 30}]},
                                "speed.swimming": {"apply": "replace", "expr": [{"const": 25}]}}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "powerful build (carries/pushes as one size larger)",
                    "predatory instincts (advantage on perception and survival checks related to hunting/tracking)",
                    "silent movement (footsteps don't produce noise)"
                ]}]}
            }
        },
        "Onicronimb": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 2}]},
                "constitution": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": ["cold", "fire"]}]},
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "jumping spider heritage (can jump up to 30ft horizontally and 15ft vertically)",
                    "wall-climbing (can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check)"
                ]}]}
            }
        },
        "Octolen": {
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 2}]},
                "intelligence": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "other_physical_features": {"apply": "add", "expr": [{"const": [
                    "tentacled lower body (can use tentacles for manipulation and movement, for 8 limbs total)",
                    "amphibious (breaths air and water)",
                    "ink secretion (can release ink to obscure vision in a 10ft radius once per short rest)"
                ]}]}
            }
        },
        "Browish": {
            "core_combat": {
                "ac": {"apply": "add", "expr": [{"const": 2}]},
                "size": {"apply": "replace", "expr": [{"const": Size.LARGE}]}
            },
            "ability_scores": {
                "strength": {"apply": "add", "expr": [{"const": 2}]},
                "constitution": {"apply": "add", "expr": [{"const": 1}]}
            },
            "other_info": {
                "resistances": {"apply": "add", "expr": [{"const": "cold"}]}
            }
        },
        "Skullywag": {
            "ability_scores": {
                "dexterity": {"apply": "add", "expr": [{"const": 1}]},
                "charisma": {"apply": "add", "expr": [{"const": 1}]}
            },
            "proficiencies": {
                "skills": {"apply": "add", "expr": [{"const": ["performance", "sleight of hand"]}]},
                "tools": {"apply": "add", "expr": [{"const": "disguise kit"}]},
                "armors": {"apply": "replace", "expr": [{"max": [{"const": ArmorType.LIGHT}, {"stat": "armor"}]}]}
            }
        },
        "Other": {
            "ability_scores": {
                "constitution": {"apply": "add", "expr": [{"const": 1}]}
            },
            "proficiencies": {
                "weapons": {"apply": "add", "expr": [{"rd_choice": random_weapon_list}]},
                "skills": {"apply": "add", "expr": [{"rd_choice": random_skill_list}]}
            }
        }
    }

#ToDo from here
age_category = {
        "child": {
        "core_combat": {
                "speed_bonus": {"speed.walking": -5,
                                "speed.flying": -5,
                                "speed.swimming": 0,
                                "speed.climbing": -10
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
                "magic_source": {"apply": "add", "expr": [{"max": [{"const": MagicSource.INNATE}, {"stat": "magic_source"}]}]},
                "spellcasting_ability": "",
                "spell_slots": {"spell_slots.1": 0, "spell_slots.2": 0},
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

