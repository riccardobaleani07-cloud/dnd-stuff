import json, random, collections, matplotlib.pyplot as plt

# ---- Core generator (same logic as yours) ----
def generate_name(transitions, min_len, max_len):
    start_symbol = "/"
    end_symbol = "$"

    current = start_symbol if start_symbol in transitions else random.choice(list(transitions.keys()))
    name = ""

    while True:
        rand = random.random()
        cumulative = 0
        next_char = None

        for nxt, prob in transitions[current]:
            cumulative += prob
            if rand <= cumulative:
                next_char = nxt
                break

        if next_char is None:
            break

        if next_char == end_symbol:
            if len(name) >= min_len:
                break
            else:
                continue

        if next_char != start_symbol:
            name += next_char
        current = next_char

        if len(name) >= max_len:
            break

    return name.capitalize()

# ---- Simulation ----
def simulate_lengths(transitions, samples):
    length_counter = collections.Counter()

    for _ in range(samples):
        name = generate_name(transitions, random.randint(3, 5), random.randint(6, 12))
        length_counter[len(name)] += 1

    total = sum(length_counter.values())
    probabilities = {l: c / total for l, c in sorted(length_counter.items())}
    return probabilities

# ---- Load data ----
with open(r"NPC generator/npc_static_data/names_transition.json", "r", encoding="utf-8") as f:
    name_data = json.load(f)

# Choose a flavour
flavour = "Fairy"
transitions = name_data[flavour]

# ---- Run test ----
probabilities = simulate_lengths(transitions, 10000)

# ---- Print & visualize ----
for length, prob in probabilities.items():
    print(f"{length:2d} letters: {prob*100:5.2f}%")

# Optional histogram
plt.bar(probabilities.keys(), probabilities.values())
plt.xlabel("Name length")
plt.ylabel("Probability")
plt.title(f"Distribution of {flavour} name lengths (10,000 samples)")
plt.show()
