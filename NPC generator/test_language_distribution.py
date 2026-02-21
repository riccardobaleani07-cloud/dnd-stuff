import random
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from npc_static_data.data import races, language_map


def choose_race(races):
    names = [r[0] for r in races]
    weights = [r[1] for r in races]
    # Normalize weights to sum to 1
    total = sum(weights)
    weights = [w/total for w in weights]
    return random.choices(names, weights=weights, k=1)[0]


l_matrix = pd.read_csv(r"NPC generator/npc_static_data/languages_matrix.csv", index_col=0)


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
#you could test one race at a time, hust tweak the code slightly

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



