import random
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

races = [
        ("Polar Human", 0.0157),
        ("Quarryan Human", 0.0315),
        ("South Herian Human", 0.0472),     
        ("North Herian Human", 0.0472),     
        ("Plains Dorojan Human", 0.0629),   
        ("Mountains Dorojan Human", 0.0393),
        ("Common Elf", 0.0315),
        ("Dwarf", 0.0708),
        ("Dragonborn", 0.0787),
        ("Beastfolk", 0.0787),
        ("Gnome", 0.0472),
        ("Ogre", 0.0079),
        ("Half-Elf", 0.0551),
        ("Lost Goblin", 0.0016),
        ("Dark Elf", 0.0236),
        ("Aarakocra", 0.0024),
        ("Tabaxi", 0.0110),
        ("Kenku", 0.0110),
        ("Goliath", 0.0003),
        ("Celestial", 0.0002),
        ("Half-Ogre", 0.0157),
        ("Pixie", 0.0031),
        ("Turtoid", 0.0236),
        ("Triton", 0.0110),
        ("Mermaid", 0.0016),
        ("Half-Dragon", 0.0079),
        ("Insectoid", 0.0011),
        ("Lycantropus", 0.0006),
        ("Grung", 0.0008),
        ("Kling", 0.0005),
        ("Fairy", 0.0024),
        ("Satyr", 0.0005),
        ("Halfling", 0.0110),
        ("Orc", 0.0016),
        ("Tiefling", 0.0629),
        ("Yuan-Ti", 0.0031),
        ("Kobold", 0.0006),
        ("Lizardfolk", 0.0011),
        ("Aasimar", 0.0003),
        ("Firbolg", 0.0006),
        ("Bugbear", 0.0003),
        ("Hobgoblin", 0.0016),
        ("Sentient Undead", 0.0016),
        ("Moonling", 0.0079),
        ("Starborn", 0.0002),
        ("Voidling", 0.0016),
        ("Firefly", 0.0009),
        ("Shadowkin", 0.0008),
        ("Crystalborn", 0.0006),
        ("Deep-Elf", 0.0031),
        ("Wood Elf", 0.0126),
        ("Mushroomfolk", 0.0063),
        ("Sentient Construct", 0.0008),
        ("Elementalfolk", 0.0157),
        ("Plantfolk", 0.0024),
        ("True Dragon", 0.0002),
        ("Giant", 0.0002),
        ("Demon", 0.0002),
        ("Angel", 0.0002),
        ("Plasmoid", 0.0006),
        ("Demonoid", 0.0047),
        ("Spirit", 0.0013),
        ("Sylph", 0.0024),
        ("Salamanderman", 0.0041),
        ("Oni", 0.0136),
        ("Kijin", 0.0024),
        ("Majin", 0.0002),
        ("Strix", 0.0002),
        ("Changeling", 0.0016),
        ("Dryad", 0.0016),
        ("Nymph", 0.0013),
        ("Lost Sea Goblin", 0.0008),
        ("Gooba", 0.0005),
        ("True Vampire", 0.0002),
        ("Pale Knight", 0.0063),
        ("Lopunnie", 0.0325),
        ("Nightmare", 0.0002),
        ("Wisp", 0.0002),
        ("Moonskin Elf", 0.0246),
        ("Spectre", 0.0003),
        ("Banshee", 0.0002),
        ("Wolfang", 0.0031),
        ("Foxling", 0.0024),
        ("Common Birdling", 0.0071),
        ("Hybrid", 0.0036),
        ("Other", 0.0126)
        ]

    # Load the matrix for languages

def choose_race(races):
    names = [r[0] for r in races]
    weights = [r[1] for r in races]
    # Normalize weights to sum to 1
    total = sum(weights)
    weights = [w/total for w in weights]
    return random.choices(names, weights=weights, k=1)[0]


l_matrix = pd.read_csv(r"C:\Users\balea\Desktop\.py\NPC generator\languages_matrix.csv", index_col=0)

# Race → native language mapping
language_map = {
    "Polar Human": "Iceshard (Polar Humans)",
    "Quarryan Human": "Monochi (Quarryan Humans)",
    "South Herian Human": "Boulgbet (Herian Humans)",
    "North Herian Human": "Boulgbet (Herian Humans)",
    "Plains Dorojan Human": "Eclelcommon (Plains Dorojan Humans)",
    "Mountains Dorojan Human": "Naive (Mountains Dorojan Humans)",
    "Half-Elf": "Elvish",
    "Plasmoid": "Trumoid (Plasmoids)",
    "Spirit": "Enaven (Spirits)",
    "Lopunnie": "Bongy (Lopunnies)",
    "Common Birdling": "Avian (Birdlings)",
    "Hybrid": "Growl (Beastfolks)",
    "Other": "Growl (Beastfolks)",
    "Common Elf": "Elvish",
    "Dark Elf": "Drowic (Drows)",
    "Wood Elf": "Elvish",
    "Deep Elf": "Shofil (Deep Elves)",
    "Moonskin Elf": "Paleydrin (Moonskin Elves)",
    "Pixie": "Sylvan",
    "Fairy": "Sylvan",
    "Firbolg": "Goblin",
    "Elementalfolk": "Ancient Primordial",
    "Sylph": "Sylph",
    "Dryad": "Dryadic",
    "Gnome": "Gnim",
    "Dwarf": "Dwarvish",
    "Tabaxi": "Tabaxi",
    "Kenku": "Crowden (Kenkus)",
    "Goliath": "Gol-Kaa (Goliaths)",
    "Beastfolk": "Clorphine (Beastfolks)",
    "Satyr": "Faun",
    "Bugbear": "Goblin",
    "Sentient Construct": "Bit-Byte (Sentient Constructs)",
    "Giant": "Giant",
    "Wolfang": "Wolfang",
    "Dragonborn": "Draconic",
    "Half-Dragon": "Draconic",
    "True Dragon": "Draconic",
    "Kobold": "Yipyak",
    "Lizardfolk": "Draconic",
    "Firefly": "Ferish (Fireflies)",
    "Pale Knight": "Paladrin (Pale Knights)",
    "Lost Goblin": "Goblin",
    "Hobgoblin": "Goblin",
    "Lost Sea Goblin": "Goblin",
    "Mushroomfolk": "Mushrik (Mushroomfolk)",
    "Ogre": "Ogrish",
    "Half-Ogre": "Ogrish",
    "Insectoid": "Netfery (Insectoids)",
    "Grung": "Grung",
    "Kling": "Kling (Klings)",
    "Halfling": "Luiric",
    "Orc": "Orcish",
    "Plantfolk": "Leafly (Plantfolk)",
    "Tiefling": "Infernal",
    "Demonoid": "Abyssal",
    "Yuan-Ti": "Yuan-Tish (Yuan-Ti)",
    "Demon": "Abyssal",
    "Salamanderman": "Larsh (Salamandermen)",
    "Oni": "Oopkni (Oni people)",
    "Kijin": "Snept (Kijin people)",
    "Majin": "Ancient Primordial",
    "Strix": "Strict (Strixes)",
    "Nightmare": "Shriek (Nightmares)",
    "Celestial": "Celestial",
    "Angel": "Celestial",
    "Aarakocra": "Aarakocra",
    "Aasimar": "Celestial",
    "Moonling": "Moonlight (Moonlings)",
    "Foxling": "Vulpin (Foxlings)",
    "Shadowkin": "Darkspeak (Shadowkins)",
    "Wisp": "Auran",
    "Voidling": "Voshedi (Voidlings)",
    "Lycantropus": "Growl (Beastfolks)",
    "Sentient Undead": "Dark Speech",
    "Starborn": "Flashmy (Starborns)",
    "Crystalborn": "Pick Neet (Crystalborn)",
    "Changeling": "Sylvan",
    "True Vampire": "Echosnhachy (True Vampires)",
    "Spectre": "Dark Speech",
    "Triton": "Abyssal",
    "Mermaid": "Abyssal",
    "Nymph": "Sylvan",
    "Turtoid": "Turtoid (Turtoids)",
    "Gooba": "Goo Bee Nie (Gooba)",
    "Banshee": "Elvish",
}

def pick_languages(race):
    # Returns list of languages an NPC might know.
    native_lang = language_map.get(race, "Gibberish/Mute")
    if native_lang not in l_matrix.index:
        return [native_lang]
    
    weights = l_matrix.loc[native_lang]
    known = {native_lang}
    for lang, weight in weights.items():
        # Roll for each possible neighbour
        if random.random() < weight:
            known.add(lang)
        
    return known

    
# ---------- Simulation ----------
n_trials = 1000  # more trials = smoooooooother stats
# u could test one race at a time, hust tweak the code slightly

results = []
for _ in range(n_trials):
    results.append(pick_languages(choose_race(races)))

# Flatten all results for global language probability
all_langs = [lang for group in results for lang in group]
lang_counts = Counter(all_langs)
lang_probs = {lang: count / n_trials for lang, count in lang_counts.items()}

# Count how many languages per NPC
size_counts = Counter(len(group) for group in results)
size_probs = {size: count / n_trials for size, count in size_counts.items()}


#---------- Output ----------
print(f"\n=== general language statistics ===")
print("Probability of knowing each language:")
for lang, prob in sorted(lang_probs.items(), key=lambda x: -x[1]):
    print(f"{lang:25s}: {prob:.3f}")

print("\nProbability of knowing N languages:")
for n, prob in sorted(size_probs.items()):
    print(f"{n} languages: {prob:.3f}")



# ---------- Graph 1: Probability of knowing each language ----------
langs = list(lang_probs.keys())
probs = [lang_probs[l] for l in langs]

plt.figure(figsize=(12, 6))
plt.bar(langs, probs, color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Probability")
plt.title(f"Probability of knowing each language")
plt.tight_layout()
plt.show()


# ---------- Graph 2: Probability of knowing N languages ----------
sizes = list(size_probs.keys())
size_prob_values = [size_probs[s] for s in sizes]

plt.figure(figsize=(8, 5))
plt.bar(sizes, size_prob_values, color="salmon")
plt.xlabel("Number of languages known")
plt.ylabel("Probability")
plt.title(f"Probability distribution of number of languages")
plt.xticks(sizes)
plt.tight_layout()
plt.show()



