from npc_static_data.enums import Size, MagicSource, ArmorType
import random


# --- Core combat and progression ---
hp = 10                   # depends on CON (and maybe race, size, level)
ac = 10                   # base 10, modified by DEX, armor, and possibly race
initiative = 0            # equals DEX mod (+ race or feats if you add them later)
speed = {"walking": 30,
        "flying": 0,
        "swimming": 0,
        "climbing": 0}    # race-based primarily, possibly age-based
level = 1                 # influences proficiency and class-like features
size = Size.MEDIUM        # depends on race and age category

proficiency_bonus = 2     # directly derived from level

# --- Ability scores and modifiers ---
strength = 10             # race and age category affect
strength_mod = 0          # derived from strength
dexterity = 10            # race and age category affect
dexterity_mod = 0         # derived from dexterity
constitution = 10         # race and age category affect
constitution_mod = 0      # derived from constitution
intelligence = 10         # race and age category affect
intelligence_mod = 0      # derived from intelligence
wisdom = 10               # race and age category affect
wisdom_mod = 0            # derived from wisdom
charisma = 10             # race and age category affect
charisma_mod = 0          # derived from charisma

# --- Proficiencies ---
weapons = []              # race, background, occupation
armors = ArmorType.UNARMORED# race, background, occupation
tools = []                # race, background, occupation
skills = []               # race, background, occupation
saving_throws = []        # race, background, occupation

# --- Magic ---
magic_source = MagicSource.NONE       # race, background, occupation (can be none, innate (spellcasting ability not required) or learned; those three parameters have power on each other in that order)
spellcasting_ability = random.choice(["wisdom", "intelligence", "charisma"]) # race, background, occupation
spell_save_dc = 0         # = 8 + prof_bonus + spellcasting ability mod
spell_attack_bonus = 0    # = prof_bonus + spellcasting ability mod
spell_slots = {"1": 0,
               "2": 0,
               "3": 0,
               "4": 0,
               "5": 0,
               "6": 0,
               "7": 0,
               "8": 0,
               "9": 0,
               "10": 0} # race, background, occupation
known_spells = []         # race, background, occupation
known_cantrips = []        # race, background, occupation

# --- Other DM-facing info ---
passive_perception = 10      # = 10 + WIS mod (+ proficiency if applicable)
add_advantage_on = []            # race, background
add_disadvantage_on = []         # race, background
resistances = []             # race, background
immunities = []              # race
vulnerabilities = []         # race
other_physical_features = [] # race
equipment = []               # occupation, background, wealth level
overall_cr = 0.125           # manual input or computed later