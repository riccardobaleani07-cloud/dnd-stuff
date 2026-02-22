import random
from collections import Counter
from npc_static_data import data

def infer_reputation_from_personality(traits):

    trait_map = data.trait_to_reputation.copy()
    types = data.reputation_types.copy()

    for trait in traits:
        if trait in trait_map:
            for rep_type, score in trait_map[trait].items():
                types[rep_type] += score

    sorted_reputations = sorted(types.items(), key=lambda x: x[1], reverse=True)
    top_reputations = [rep for rep, score in sorted_reputations if score == sorted_reputations[0][1]]
    return random.choice(top_reputations)

# Run 5000 tests
trait_list = data.default_traits.copy()

results = []
for _ in range(100000):
    num_traits = 3
    selected_traits = random.sample(trait_list, num_traits)
    reputation = infer_reputation_from_personality(selected_traits)
    results.append(reputation)
reputation_counts = Counter(results)
for reputation, count in reputation_counts.items():
    print(f"{reputation}: {count}")
# Example output:
# Lovely: 450
# Respectful: 600
# Etc.