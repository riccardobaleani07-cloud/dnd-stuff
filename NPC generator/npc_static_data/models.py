from dataclasses import dataclass

@dataclass
class NPC:
    def __init__(self, name, gender, race, subtype, language, occupation, age_category, age, alignment, partnership, personality_traits, offsprings, reputation, wealth, backstory_seed, social_level, backstory):

        self.name = name
        self.gender = gender
        self.race = race
        if subtype != None:
            self.subtype = subtype
        else:
            self.subtype = ""
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

    def __str__(self):
        return (
            f"--- NPC Profile ---\n"
            f"Name and Surname: {self.name}\n"
            f"Gender: {self.gender}\n"
            f"Race and Eventual Subtype: {self.race} {self.subtype}\n"
            f"Language: {self.language}\n\n"
            f"Social Level: {self.social_level.name.capitalize()}\n"
            f"Occupation: {self.occupation}\n\n"
            f"Age: {self.age} ({self.age_category})\n"
            f"alignment: {self.alignment}\n"
            f"Partnership Status: {self.partnership}\n"
            f"Number of Descendants: {self.offsprings}\n\n"
            f"Personality Traits: {', '.join(self.personality_traits)}\n"
            f"Reputation: {self.reputation}\n"
            f"Wealth: {self.wealth.name.capitalize()}\n\n"
            f"Backstory Seed: {self.backstory_seed}\n"
            f"-----Backstory-----\n{self.backstory}\n"
            f"-------------------"
        )