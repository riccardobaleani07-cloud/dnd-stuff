from dataclasses import dataclass
from collections import Counter
from enum import IntEnum


@dataclass
class NPC:
    def __init__(
        self,
        name,
        gender,
        race,
        subtype,
        language,
        occupation,
        age_category,
        age,
        alignment,
        partnership,
        personality_traits,
        offsprings,
        reputation,
        wealth,
        backstory_seed,
        social_level,
        backstory,
        stats=None
    ):
        self.name = name
        self.gender = gender
        self.race = race
        self.subtype = subtype if subtype is not None else ""
        self.language = language
        self.age_category = age_category
        self.age = age
        self.occupation = occupation
        self.alignment = alignment
        self.partnership = partnership
        self.personality_traits = personality_traits
        self.offsprings = offsprings
        self.reputation = reputation
        self.wealth = wealth
        self.backstory_seed = backstory_seed
        self.social_level = social_level
        self.backstory = backstory
        self.stats = stats

    def _format_number(self, value):
        """Round numbers using the NPC generator's 0.6 threshold."""

        if isinstance(value, IntEnum):
            return value

        if isinstance(value, float):
            integer = int(value)

            if value - integer >= 0.6:
                return integer + 1

            return integer

        return value

    def _format_value(self, value):
        if isinstance(value, IntEnum):
            return value.name.replace("_", " ").capitalize()

        if isinstance(value, (int, float)):
            return str(self._format_number(value))

        if isinstance(value, list):
            return self._format_list(value)

        if isinstance(value, dict):
            return self._format_dict(value)

        if isinstance(value, tuple):
            return str(value)

        return str(value)

    def _format_list(self, values):
        """Format lists while grouping identical elements."""

        if not values:
            return "None"

        counts = Counter(values)

        result = []

        for value, count in counts.items():
            formatted = self._format_value(value)

            if count == 1:
                result.append(formatted)
            else:
                result.append(f"{count} × {formatted}")

        return ", ".join(result)

    def _format_dict(self, values):
        """Format nested dictionaries."""

        lines = []

        for key, value in values.items():
            formatted_key = key.replace("_", " ").capitalize()
            formatted_value = self._format_value(value)

            lines.append(f"{formatted_key}: {formatted_value}")

        return "\n".join(lines)

    def _format_stats(self):
        """Format the generated NPC statistics."""

        if not self.stats:
            return "No statistics generated."

        lines = []

        sections = {
            "Core Combat": [
                "level",
                "proficiency_bonus",
                "hp_dice",
                "hp",
                "ac",
                "initiative",
                "size",
                "speed",
            ],

            "Ability Scores": [
                "strength",
                "strength_mod",
                "dexterity",
                "dexterity_mod",
                "constitution",
                "constitution_mod",
                "intelligence",
                "intelligence_mod",
                "wisdom",
                "wisdom_mod",
                "charisma",
                "charisma_mod",
            ],

            "Proficiencies": [
                "weapons",
                "armors",
                "tools",
                "skills",
                "saving_throws",
            ],

            "Magic": [
                "magic_source",
                "spellcasting_ability",
                "spellcasting_ability_mod",
                "spell_slots",
                "known_spells",
                "known_cantrips",
                "spell_attack_bonus",
                "spell_save_dc",
            ],

            "Other": [
                "equipment",
                "resistances",
                "immunities",
                "vulnerabilities",
                "add_advantage_on",
                "add_disadvantage_on",
                "other_physical_features",
                "passive_perception",
                "overall_cr",
            ],
        }

        for section, stat_names in sections.items():
            section_lines = []

            for stat_name in stat_names:
                if stat_name not in self.stats:
                    continue

                value = self.stats[stat_name]

                # Don't print empty lists
                if isinstance(value, list) and not value:
                    continue

                # Don't print empty dictionaries
                if isinstance(value, dict) and not value:
                    continue

                display_name = stat_name.replace("_", " ").capitalize()

                if isinstance(value, dict):
                    section_lines.append(
                        f"{display_name}:\n"
                        + "\n".join(
                            f"  {k}: {self._format_value(v)}"
                            for k, v in value.items()
                            if not isinstance(v, list) or v
                        )
                    )
                else:
                    section_lines.append(
                        f"{display_name}: {self._format_value(value)}"
                    )

            if section_lines:
                lines.append(f"\n[{section}]")
                lines.extend(section_lines)

        return "\n".join(lines)

    def __str__(self):
        return (
            f"--- NPC Profile ---\n"
            f"Name and Surname: {self.name}\n"
            f"Gender: {self.gender}\n"
            f"Race and Eventual Subtype: {self.race} {self.subtype}\n"
            f"Language: {self.language}\n\n"

            f"Social Level: {self.social_level.name.capitalize()}\n"
            f"Occupation: {self.occupation['display']}\n\n"

            f"Age: {self.age} ({self.age_category})\n"
            f"Alignment: {self.alignment}\n"
            f"Partnership Status: {self.partnership}\n"
            f"Number of Descendants: {self.offsprings}\n\n"

            f"Personality Traits: {', '.join(self.personality_traits)}\n"
            f"Reputation: {self.reputation}\n"
            f"Wealth: {self.wealth.name.capitalize()}\n\n"

            f"Backstory Seed: {self.backstory_seed}\n"
            f"----- Backstory -----\n"
            f"{self.backstory}\n"
            f"---------------------\n"

            f"{self._format_stats()}\n"
            f"---------------------"
        )