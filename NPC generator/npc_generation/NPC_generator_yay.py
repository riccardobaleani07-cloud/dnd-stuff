#NPC generator, yay

#imports
import random
import json
import pandas as pd
from npc_static_data.enums import Size, SocialLevel, Wealth, MagicSource, ArmorType
from npc_static_data import data
from npc_static_data import models
from npc_static_data import base_stats
from enum import Enum, IntEnum, auto





class NPCGenerator:

    # I define class-level constants just before a function needs them
    # But all the big data structures can be found in npc_static_data/data.py


    # From this point on i handle the generation of stats tied to the roleplay

    def generate_backstory(self, seed, name, age_category, race):
        flavour = data.backstory_flavour.get(seed)
        if flavour is None:
            raise ValueError(f"No backstory flavour found for seed '{seed}'")

        templates = data.bc_flavour_to_templates.get(flavour)
        if not templates:
            raise ValueError(f"No templates found for backstory flavour '{flavour}'")
        template = random.choice(templates)

        seed_data = data.seed_global_data.get(seed)
        if seed_data is None:
            raise ValueError(f"No origin data found for backstory seed '{seed}'")

        origin = random.choice(seed_data.get("origin", ["an unknown past"]))
        catalyst = random.choice(seed_data.get("catalyst", ["a mysterious event"]))
        drive = random.choice(seed_data.get("drive", ["continue their journey"]))

        story = template.format(
            name=name,
            age_category=age_category,
            race=race,
            origin=origin,
            catalyst=catalyst,
            drive=drive
        )

        optional_placeholders = {
            "oath": data.oaths.copy(),
            "fallen_city": data.fallen_cities.copy(),
            "war_event": data.war_event.copy(),
            "disaster": data.disasters.copy(),
        }

        for placeholder, choices in optional_placeholders.items():
            story = story.replace(f"{{{placeholder}}}", random.choice(choices))

        return story.strip()

    def choose_social_level(self, social_levels: list[tuple[SocialLevel, float]]) -> SocialLevel:
        levels = [level for level, weight in social_levels]
        weights = [weight for level, weight in social_levels]
        total = sum(weights)
        normalized = [w / total for w in weights]
        return random.choices(levels, weights=normalized, k=1)[0]
        
    def choose_race(self, races):
        names = [r[0] for r in races]
        weights = [r[1] for r in races]
        # Normalize weights to sum to 1
        total = sum(weights)
        weights = [w/total for w in weights]
        return random.choices(names, weights=weights, k=1)[0]
    
    def conditional_choose_subtype (self, available_subtypes, race):
        # Chooses a subtype if applicable
        for ar in available_subtypes:
            if ar[0] == race:
                names = [sr[0] for sr in ar[1]]
                weights = [sr[1] for sr in ar[1]]
                # Normalize weights to sum to 1
                total = sum(weights)
                weights = [w/total for w in weights]
                return random.choices(names, weights=weights, k=1)[0]
        return None
        
    def choose_gender(self, genders, race, species_gender_map):
        # Chooses a gender, crafting a pool based on race
        # Default gender pool and weights
        # The default pool is used as a baseline: rare genders are added, and default genders are removed if necessary
        default_pool = genders
        default_weights = [10000, 10000, 1, 5] # order:Male, Female, Lost, Androgine
        # weights do not need to sum to 1; random.choices normalizes them
        
        # Rare genders mapped to applicable species (placeholder example)

        # Build the gender pool
        pool = list(default_pool)

        for gender, species_list in species_gender_map.items():
            if race in species_list:
                if gender in pool:
                    pool.remove(gender)   # remove default
                else:
                    pool.append(gender)   # add rare gender
        # The design intentionally allows for a pool with only rare genders
        # The design is not meant to flow equally among all genders: some are always added while others are alwaysremoved


        # Assign default weights for the current pool
        # Rare genders can get fixed weights or proportional scaling
        weights = []
        for g in pool:
            if g in ["Male", "Female", "Lost", "Androgine"]:
                weights.append(default_weights[default_pool.index(g)])
            else:
                # Assign a small fixed weight for rare genders
                weights.append(9000)  # shared weight by rare genders

        # Pick a gender
        return random.choices(pool, weights=weights, k=1)[0]

    def generate_age_and_category(self, race, race_age_ranges):
        # Return (age_category, age) based on race-specific distributions
        

        age_category = random.choices(
            population=list(race_age_ranges[race].keys()),
            weights=[3, 2, 3, 2, 1],  # Probabilities to favour certain age groups
            k=1
        )[0]
        age_min, age_max = race_age_ranges[race][age_category]
        age = random.randint(age_min, age_max)
        return age_category, age

    def generate_partnership(self, age_category, options_by_age):
        choices = list(options_by_age[age_category].keys())
        weights = list(options_by_age[age_category].values())
        return random.choices(choices, weights=weights, k=1)[0]

    def generate_num_descendants(self, age_category, partnership, distribution_settings):

        modifier = 1.0

        low, high, mode = distribution_settings[age_category]
        base_descendants = random.triangular(low, high, mode)

        #hack to prevent negative descendants
        if base_descendants <= 0:
            base_descendants = 0

        # Modify by partnership
        if partnership:
            if "Married" in partnership or "Engaged" in partnership:
                if age_category != "teen":
                    modifier = 1.5
            elif ("Widow" in partnership or "Lifelong Partner" in partnership):
                modifier = 1.4
            else:
                modifier = 0.6
        
        base_descendants = int(round(base_descendants * modifier))
        return base_descendants

    def generate_occupation(self, social_level, age_category, occupations_by_social, exotic, age_weights):

        # Choose the employment stage for this age
        stage_choices = list(age_weights[age_category].keys())
        stage_weights = list(age_weights[age_category].values())
        employment_stage = random.choices(stage_choices, weights=stage_weights, k=1)[0]


        # Choose the job for this social level
        job_choices = list(occupations_by_social[social_level].keys())
        job_weights = list(occupations_by_social[social_level].values())
        job = random.choices(job_choices, weights=job_weights, k=1)[0]

        # If job is Exotic, pick a specific exotic job
        if job == "Exotic":
            job_choices = list(exotic.keys())
            job_weights = list(exotic.values())
            job = random.choices(job_choices, weights=job_weights, k=1)[0]

        # Build the output depending on stage
        if "Unemployed" in employment_stage or "Minor Duties" in employment_stage:
            # Output format: “Employment Stage”, e.g., “Unemployed” or “Minor Duties”
            occupation = employment_stage
        elif "Retired" in employment_stage or "Advisor" in employment_stage:
            # Output format: “Employment Stage (Last known occupation: Job)”, e.g., “Retired (Last known occupation: Blacksmith)” or “Advisor (Last known occupation: Healer)”
            occupation = f"{employment_stage} (Last known occupation: {job})"
        else:
            # Output format: “Employment Stage (Job)”, e.g., “Apprentice/Student (Blacksmith)” or “Full-time Occupation (Healer)”
            occupation = f"{employment_stage} ({job})"

        return {
            "stage": employment_stage,
            "job": job if "Unemployed" not in employment_stage and "Minor Duties" not in employment_stage else None,
            "display": occupation  # keep your string for UI
        }

    def generate_wealth(self, social_level: SocialLevel, wealth_ranges) -> Wealth:
        low, high = wealth_ranges[social_level]
        return Wealth(random.randint(low, high))

    personality_traits_count = 3
    def generate_personality_traits(self, personality_traits_count, default_traits):
        # Return a list of personality traits
        
        traits = random.sample(default_traits, k=personality_traits_count)
        return traits
    
    def infer_alignment_from_personality(self, traits, good_traits, evil_traits, lawful_traits, chaotic_traits):

        #Good is counted as positive, Evil as negative
        good_evil_score = 0
        for trait in traits:
            if trait in good_traits:
                good_evil_score += 1
            elif trait in evil_traits:
                good_evil_score -= 1

        #Lawful is counted as positive, Chaotic as negative
        lawful_chaotic_score = 0
        for trait in traits:
            if trait in lawful_traits:
                lawful_chaotic_score += 1
            elif trait in chaotic_traits:
                lawful_chaotic_score -= 1
        
        # Determine alignment based on scores
        if good_evil_score > 0:
            alignment = "Good"
        elif good_evil_score < 0:
            alignment = "Evil"
        else:
            alignment = "Neutral"
        
        if lawful_chaotic_score > 0:
            alignment = f"Lawful {alignment}"
        elif lawful_chaotic_score < 0:
            alignment = f"Chaotic {alignment}"
        else:
            if alignment == "Neutral":
                alignment = "True Neutral"
                #Special case for pure neutral
            else:
                alignment = f"Neutral {alignment}"
        
        
        return alignment
    
    def infer_reputation_from_personality(self, traits, reputation_types, trait_to_reputation):
        
        # Adjust reputation scores based on personality traits
        for trait in traits:
            if trait in trait_to_reputation:
                adjustments = trait_to_reputation[trait]
                for rep_type, score in adjustments.items():
                    reputation_types[rep_type] += score
        # Determine the top 2 reputation types
        sorted_reputations = sorted(reputation_types.items(), key=lambda x: x[1], reverse=True)
        top_reputations = [rep for rep, score in sorted_reputations if score == sorted_reputations[0][1]]
        # If multiple top reputations, randomly select one
        reputation = random.choice(top_reputations)
        return reputation

    # Data extractor for mapping letters
    with open(r"NPC generator/npc_static_data/names_transition.json", "r", encoding="utf-8") as f:
        name_data = json.load(f)

    # Word assembler
    def generate_name(self, transitions, min_len, max_len):
        start_symbol = "/"
        end_symbol = "$" # It is encoded in the json file as a possible next character
        vowels = set("aeiouyáéíóúýàèìòùäëû")
        
        current = start_symbol
        name = ""
        consonant_streak = 0

        while True:
            if current not in transitions:
                if len(name) >= min_len:
                    break
                else:
                    name += random.choice(["'", "-", " "])
                    current = start_symbol
                    consonant_streak = 0
                    continue

            # Get next transition
            rand = random.random()
            cumulative = 0
            next_char = None

            for nxt, prob in transitions[current]:
                cumulative += prob
                if rand <= cumulative:
                    next_char = nxt
                    break

            if not next_char:
                break

            if next_char == end_symbol:
                if len(name) >= min_len:
                    break
                else:
                    continue

            # If we've had too many consonants, force a vowel
            if consonant_streak >= 2:
                available_next = {n for n, _ in transitions[current]}
                possible_vowels = [v for v in vowels if v in transitions]
                if possible_vowels:
                    next_char = random.choice(possible_vowels)
                else:
                    next_char = random.choice(list(vowels))
                consonant_streak = 0  # reset after forcing a vowel

            # Add the letter
            if next_char != start_symbol:
                name += next_char

            # Update consonant streak
            if next_char in vowels:
                consonant_streak = 0
            else:
                consonant_streak += 1

            current = next_char

            # Safety cutoff
            if len(name) >= max_len:
                break

        return name.title() # good capitalizations for fantasy names

    # Actual name generating function
    def generate_npc_name(self, race, with_surname=True):
        flavour = data.flavour_map.get(race, "Human")
        transitions = self.name_data.get(flavour, {})
        if not transitions:
            return "Nameless"

        first = self.generate_name(transitions, random.randint(3, 5), random.randint(6, 12))
        if with_surname:
            surname = self.generate_name(transitions, random.randint(3, 7), random.randint(8, 12))
            return f"{first} {surname}"
        return first

    # Load of the matrix for languages
    l_matrix = pd.read_csv(r"NPC generator/npc_static_data/languages_matrix.csv", index_col=0)

    def pick_languages(self, race):
        # Returns list of languages an NPC might know.
        native_lang = data.language_map.get(race, "Gibberish/Mute")
        if native_lang not in self.l_matrix.index:
            return [native_lang]
        
        weights = self.l_matrix.loc[native_lang]
        known = {native_lang}
        for lang, weight in weights.items():
            # Roll for each possible neighbour
            if random.random() < weight: #toFix: strange error: TypeError: '<' not supported between instances of 'float' and 'str'
                known.add(lang)
        
        return ", ".join(known)



    # From this point on i'll handle common stats useful for DMs


    # ToDo: logic to generate raw stats stated above, based on the npc_static_data/modifiers.py file
    # The approach will be simple: the order of generation is relevant to what has more importance
    # The initialized values are not placeholders: they are the base for a generic humanoid, and the generation process is only going to modify them, almost never overriding.
    # For now level will be left at 1, but the logic will be still implemented for a few attributes.
    # List of things i can generate instantly: speed, level, size, raw ability scores, all proficiencies, magic_source, spellcasting_ability, spell_slots, known_spells, known_cantrips, advantage_on, disadvantage_on, every other dm-facing info (except the CR and the passive_perception)
    # I aim to cycle through each sub-section three times max: 1 to find the right race/occupation/background/etc, 2 to compute all of the above, 3 to compute the rest.
    # It is very probabile that between step 2 and 3 i need a finalization of some stats before applying other modifiers.

    # Evaluating function: given a list expression, it will return the evaluated result following the rules of the modifiers.py file.
    # Example expressions: [{"min": [{"stat": "armors"}, {"const": ArmorType.LIGHT}]}]
    #                      [{"rd_choice": [{"stat": "tools"}]}, {"rd_choice": [{"stat": "tools"}]}, {"rd_choice": [{"stat": "tools"}]}]    

    # Operational functions

    def _key(self, v):
        if isinstance(v, (int, float)):
            return (0, v)

        if isinstance(v, tuple) and len(v) == 3:
            val, ttype, measure = v
            return (1, ttype, measure, val)

        # fallback: everything else is lowest priority
        return (2, str(v))

    def _partition(self, values):
        nums = []
        strings = []
        lists = []
        tuples = []
        others = []

        for v in values:

            # bools are treated as numbers (0 or 1)
            if isinstance(v, bool):
                nums.append(int(v))

            # numeric primitives
            elif isinstance(v, (int, float)):
                nums.append(v)

            # ordered enums (IntEnum or numeric Enum)
            elif isinstance(v, IntEnum):
                nums.append(v.value)

            elif isinstance(v, str):
                strings.append(v)

            elif isinstance(v, list):
                lists.append(v)

            elif isinstance(v, tuple) and len(v) == 3:
                tuples.append(v)

            else:
                others.append(v)

        return nums, strings, lists, tuples, others

    def op_add(self, values):

        nums, strings, lists, tuples, others = self._partition(values)

        result = []

        # numbers
        if nums:
            result.append(sum(nums))
            # print(f"Debug: Adding numbers {nums} -> {sum(nums)}")


        merged = []
        # strings
        if strings:
            for s in strings:
                merged.append(s)
            # print(f"Debug: Adding strings {strings} -> {merged} -> {result}")

        # lists
        if lists:
            for l in lists:
                for item in l:
                    merged.append(item)
            # print(f"Debug: Adding lists {lists} -> {merged} -> {result}")

        result.extend(merged)

        # tuples (only first field, type/measure preserved)
        if tuples:
            # print(f"Debug: Adding tuples {tuples}")
            # only works if same (type, measure)
            grouped = {}
            for ttype, val, measure in tuples:
                key = (ttype)
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(val)

            for (ttype), vals in grouped.items():
                result.append((ttype, sum(vals), measure))

        # others (passthrough)
        result.extend(others)
        # print(f"Debug: Adding others {others} -> {result}")

        return result

    def op_multiply(self, values):

        nums, strings, lists, tuples, others = self._partition(values)

        # 1. compute factor
        factor = 1
        for n in nums:
            factor *= n

        # normalize factor to integer for repeat counts
        try:
            factor_count = int(round(factor))
        except Exception:
            print(f"Warning: factor {factor} is not a valid integer, defaulting to 1")
            factor_count = 1

        result = []

        # 2. strings (repeat)
        for s in strings:
            for factor_count in range(factor_count):
                result.append(s)

        # 3. lists (intersection)
        if lists:
            # print(f"Debug: lists to intersect: {lists}")
            if len(lists) == 1:
                for factor_count in range(factor_count):
                    result.append(lists[0])
            else:
                merged = lists[0]
                for l in lists:
                    merged = list(set(merged) & set(l))
                    # print(f"Debug: merged list after intersection: {merged}")

                for factor_count in range(factor_count):
                    result.extend(merged)
                    

        # 4. tuples (scale first field only)
        for val, ttype, measure in tuples:
            result.append((ttype, val * factor_count, measure))

        # 5. keep numeric result if nothing else is present
        if  not lists and not strings and not tuples:
            result.append(factor_count)

        # 6. others untouched
        result.extend(others)

        return result

    def op_divide(self, values):

        nums, strings, lists, tuples, others = self._partition(values)

        result = []

        # 1. numeric divisor
        divisor = 1
        for n in nums:
            if n == 0:
                print(f"Warning: division by zero encountered in values {values}, skipping this value")
                continue
            divisor /= n

        if divisor == 0:
            print(f"Warning: final divisor is zero after processing values {values}, defaulting to 1")
            divisor = 1

        # print(f"Debug: Divisor computed as {divisor} from values {nums}")

        # 2. strings (probabilistic retention)
        kept = []
        for s in strings:
            if random.random() < divisor:
                kept.append(s)
            
        result.extend(kept)

        # 3. lists output the simmetric difference of all lists
        if lists:
            # print(f"Debug: lists to reduce: {lists}")
            if len(lists) == 1:
                for item in lists[0]:
                    if random.random() < divisor:
                        result.append(item)
            else:
                merged = lists[0]
                # print(f"Debug: initial merged list: {merged}")
                for l in lists[1:]:
                    # print(f"Debug: symmetric difference between {merged} and {l}: {list(set(merged) ^ set(l))}")
                    merged = list(set(merged) ^ set(l))
                    # print(f"Debug: merged list after reduction: {merged}")

                for item in merged:
                    if random.random() < divisor:
                        result.append(item)

        # 4. tuples (divide first field)
        for val, ttype, measure in tuples:
            result.append((ttype, val * divisor, measure))

        # 5. keep numeric result if nothing else is present
        if not lists and not strings and not tuples:
            result.append(divisor)

        # 6. others unchanged
        result.extend(others)

        return result

    def op_min(self, values):

        if not values:
            return []

        best = min(values, key=self._key)
        return [best]

    def op_max(self, values):

        if not values:
            return []

        best = max(values, key=self._key)
        return [best]

    def resolve_stat(self, values):

        # if len(values) != 1:
        #     raise ValueError(f"stat expects exactly 1 argument, got {values}")

        path = values

        if not isinstance(path, str):
            raise TypeError("stat expects a string path")

        parts = path.split(".")
        current = base_stats

        for p in parts:
            if isinstance(current, dict):
                if p not in current:
                    raise KeyError(f"Unknown stat: {path}")
                current = current[p]
            else:
                # accessing attribute of imported objects (Enum, etc.)
                if not hasattr(current, p):
                    raise KeyError(f"Invalid substat access: {path}")
                current = getattr(current, p)

        # IMPORTANT RULE:
        # disallow partial resolution of structured containers
        if isinstance(current, dict):
            raise ValueError(f"Cannot resolve partial stat group: {path}")

        return current

    # Routing functions
    def _flatten(self, value):
        result = []
        for v in value:
            result.extend(self.evaluate(v))
        return result

    def evaluate(self, expr):

        # 1. list = operand container
        if isinstance(expr, list):
            result = []
            for e in expr:
                result.extend(self.evaluate(e))
            return result

        # 2. atomic value
        if not isinstance(expr, dict):
            return [expr]   # ALWAYS list-wrapped

        # 3. operator node
        op, value = next(iter(expr.items()))

        # ---------------- CONST ----------------
        if op == "const":
            return [value]

        # ---------------- STAT ----------------
        if op == "stat":
            return [self.resolve_stat(value)]

        # ---------------- MIN ----------------
        if op == "min":
            vals = self._flatten(value)
            return self.op_min(vals) if vals else []

        # ---------------- MAX ----------------
        if op == "max":
            vals = self._flatten(value)
            return self.op_max(vals) if vals else []

        # ---------------- RD CHOICE ----------------
        if op == "rd_choice":
            vals = value
            return  self._flatten([random.choice(vals)] if vals else [])

        # ---------------- ADD ----------------
        if op == "add":
            vals = self._flatten(value)
            return self.op_add(vals) if vals else []

        # ---------------- MULTIPLY ----------------
        if op == "multiply":
            vals = self._flatten(value)
            return self.op_multiply(vals) if vals else []

        # ---------------- DIVIDE ----------------
        if op == "divide":
            vals = self._flatten(value)
            return self.op_divide(vals) if vals else []

        raise ValueError(f"Unknown operation: {op}")


    def generate_npc(self):
        race = self.choose_race(data.races)
        language = self.pick_languages(race)
        gender = self.choose_gender(data.genders, race, data.species_gender_map)
        name = self.generate_npc_name(race)
        backstory_seed = random.choice(data.backstory_seeds)
        social_level = self.choose_social_level(data.social_levels)
        age_category, age = self.generate_age_and_category(race, data.race_age_ranges)
        occupation = self.generate_occupation(social_level, age_category, data.occupations_by_social, data.exotic, data.age_weights)
        wealth = self.generate_wealth(social_level, data.wealth_ranges)
        partnership = self.generate_partnership(age_category, data.options_by_age)
        offsprings = self.generate_num_descendants(age_category, partnership, data.distribution_settings)
        personality_traits = self.generate_personality_traits(self.personality_traits_count, data.default_traits)
        alignment = self.infer_alignment_from_personality(personality_traits, data.good_traits, data.evil_traits, data.lawful_traits, data.chaotic_traits)
        reputation = self.infer_reputation_from_personality(personality_traits, data.reputation_types.copy(), data.trait_to_reputation) #reputation_types needs to be copied to avoid mutation
        backstory = self.generate_backstory(backstory_seed, name, age_category, race)
        subtype = self.conditional_choose_subtype(data.available_subtypes, race)



        return models.NPC(name, gender, race, subtype, language, occupation, age_category, age, alignment, partnership, personality_traits, offsprings, reputation, wealth, backstory_seed, social_level, backstory
                          )



