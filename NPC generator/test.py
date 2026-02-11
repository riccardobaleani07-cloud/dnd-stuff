import random
from collections import Counter

def infer_reputation_from_personality(traits):
    reputation_types = {"Lovely": 0, "Respectful": 0, "Honorable": 0, "Trustworthy": 0, "Valuable": 0, "Unknown": 0, "Mysterious": 0,
                        "Lightly Noticeable": 1, "Fearsome": 0, "Loathsome": 0, "Unreliable": 0, "Ruthless": 0, "Disgraceful": 0,
                        "Cunning": 0, "Ambiguous": 0,"Infamous": 0, "Bearable": 1, "Edgy": 0, "Charming": 0, "Dull": 0}
    
    trait_to_reputation = {
        "Brave": {"Respectful": 2, "Fearsome": 2, "Valuable": 2, "Cunning": 1, "Dull": -1, "Lightly Noticeable": -1},
        "Cautious": {"Trustworthy": 2, "Respectful": 1, "Dull": 1, "Edgy": -1, "Unknown": 1},
        "Curious": {"Mysterious": 1, "Dull": -1, "Lightly Noticeable": -1, "Ambiguous": 1, "Bearable": 1, "Lovely": 1},
        "Loyal": {"Honorable": 2, "Trustworthy": 3, "Respectful": 2, "Infamous": -1, "Loathsome": -1, "Unreliable": -1,},
        "Greedy": {"Loathsome": 1, "Cunning": 1, "Infamous": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1},
        "Honest": {"Honorable": 2, "Trustworthy": 2, "Respectful": 1, "Cunning": -1, "Ambiguous": -1, "Infamous": -1, "Loathsome": -1, "Disgraceful": -1},
        "Deceptive": {"Unreliable": 1, "Cunning": 1, "Infamous": 1, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Ambiguous": 2, "Charming": -1, "Dull": -1},
        "Charismatic": {"Charming": 3, "Lovely": 2, "Trustworthy": 1, "Loathsome": -1, "Dull": -1, "Unknown": -1, "Lightly Noticeable": -1},
        "Impulsive": {"Edgy": 1, "Fearsome": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Cunning": -1, "Unknown": -1, "Bearable": -1},
        "Reserved": {"Dull": 2, "Mysterious": 1, "Respectful": 1, "Charming": -1, "Edgy": -1, "Lightly Noticeable": -1, "Unknown": 1, "Ambiguous": 1},
        "Ambitious": {"Mysterious": 1, "Fearsome": 1, "Edgy": 1, "Cunning": 2, "Dull": -1},
        "Lazy": {"Unknown": 1, "Charming": -1, "Bearable": -1, "Honorable": -1, "Disgraceful": 1, "Loathsome": 1},
        "Friendly": {"Valuable": 2,"Lovely": 2, "Trustworthy": 2, "Charming": 2, "Dull": -1, "Mysterious": -1, "Loathsome": -1},
        "Temperamental": {"Unreliable": 1, "Charming": -1, "Dull": -1, "Respectful": -1, "Unknown": -1, "Bearable": -1,},
        "Righteous": {"Honorable": 3, "Respectful": 2, "Trustworthy": 1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Unknown": -1, "Lightly Noticeable": -1, "Dull": 1},
        "Sarcastic": {"Cunning": 2, "Edgy": 2, "Charming": 2, "Dull": -1, "Lovely": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": 1, "Mysterious": 1},
        "Arrogant": {"Loathsome": 2, "Infamous": 2, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1},
        "Protective": {"Honorable": 2, "Respectful": 2, "Trustworthy": 2, "Lovely": 1, "Fearsome": 1, "Charming": 1, "Valuable": 1},
        "Dreamy": {"Mysterious": 2, "Edgy": 1, "Dull": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Bearable": 1, "Lightly Noticeable": 1},
        "Pessimistic": {"Dull": 2, "Unknown": 1, "Bearable": -1, "Lovely": -1, "Charming": -1, "Edgy": -1},
        "Cheerful": {"Lovely": 2, "Charming": 2, "Respectful": 1, "Dull": -1, "Mysterious": -1, "Loathsome": -1},
        "Brooding": {"Mysterious": 2, "Edgy": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Lightly Noticeable": -1, "Unknown": 2, "Ambiguous": 1, "Fearsome": 1, "Loathsome": 1},
        "Stoic": {"Respectful": 1, "Honorable": 1, "Dull": 2, "Mysterious": 1, "Charming": -1, "Edgy": -1, "Lightly Noticeable": -1, "Unknown": 1, "Ambiguous": 1},
        "Generous": {"Lovely": 2, "Honorable": 2, "Trustworthy": 1, "Respectful": 1, "Cunning": -1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Charming": 1},
        "Vindictive": {"Ruthless": 2, "Infamous": 2, "Loathsome": 1, "Cunning": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1},
        "Adventurous": {"Edgy": 1, "Fearsome": 1, "Mysterious": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Lightly Noticeable": 1},
        "Meticulous": {"Respectful": 2, "Trustworthy": 2, "Honorable": 1, "Dull": 1, "Edgy": -1, "Unknown": 2},
        "Reckless": {"Fearsome": 2, "Edgy": 2, "Dull": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Ruthless": 1},
        "Optimistic": {"Lovely": 2, "Charming": 2, "Trustworthy": 1, "Respectful": 1, "Dull": -1, "Mysterious": -1, "Loathsome": -1, "Unknown": -1, "Lightly Noticeable": -1, "Disgraceful": -1},
        "Skeptical": {"Cunning": 1, "Mysterious": 1, "Dull": 1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Unreliable": 1},
        "Compassionate": {"Lovely": 2, "Honorable": 2, "Respectful": 1, "Valuable": 1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Cunning": -1},
        "Calculating": {"Cunning": 1, "Infamous": 1, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1},
        "Patient": {"Respectful": 2, "Trustworthy": 1, "Honorable": 1, "Dull": 1, "Edgy": -1, "Unknown": 2, "Lovely": 1},
        "Hot-headed": {"Edgy": 2, "Fearsome": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Cunning": -1, "Unknown": -1, "Bearable": -1, "Unreliable": 1},
        "Wise": {"Respectful": 2, "Honorable": 2, "Trustworthy": 2, "Valuable": 1, "Mysterious": 1, "Dull": 1, "Charming": -1, "Edgy": -1, "Unknown": 1},
        "Naive": {"Dull": 2, "Lovely": 1, "Charming": 1, "Respectful": 1, "Edgy": -1, "Cunning": -1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Unknown": 1, "Bearable": 1},
        "Cynical": {"Cunning": 2, "Dull": 1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Unreliable": 1},
        "Romantic": {"Charming": 3, "Lovely": 2, "Mysterious": 1, "Dull": -1, "Unknown": 1, "Lightly Noticeable": 1, "Disgraceful": -1},
        "Pragmatic": {"Respectful": 1, "Trustworthy": 2, "Cunning": 1, "Dull": 1, "Edgy": -1, "Unknown": 2},
        "Stubborn": {"Dull": 2, "Edgy": 1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Unreliable": 2},
        "Ruthless": {"Ruthless": 3, "Infamous": 2, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1},
        "Manipulative": {"Cunning": 2, "Infamous": 2, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Ruthless": 1, "Ambiguous": 2, "Charming": 1, "Dull": -1},
        "Hypercritical": {"Cunning": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 1},
        "Obsessive": {"Cunning": 2, "Edgy": 1, "Mysterious": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1},
        "Cruel": {"Edgy": 2, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 2, "Loathsome": 2, "Infamous": 1, "Ruthless": 2},
        "Fanatical": {"Ruthless": 2, "Fearsome": 1, "Loathsome": 1, "Infamous": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1, "Unreliable": 1},
        "Jealous": {"Edgy": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 2, "Loathsome": 1, "Infamous": 1},
        "Crazy": {"Mysterious": 2, "Edgy": 2, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Lightly Noticeable": -1, "Cunning": -1},
        "Eccentric": {"Mysterious": 2, "Edgy": 1, "Lovely": -1, "Charming": -1, "Dull": -1, "Unknown": 1, "Ambiguous": 1, "Lightly Noticeable": 1}
    }

    for trait in traits:
        if trait in trait_to_reputation:
            for rep_type, score in trait_to_reputation[trait].items():
                reputation_types[rep_type] += score

    sorted_reputations = sorted(reputation_types.items(), key=lambda x: x[1], reverse=True)
    top_reputations = [rep for rep, score in sorted_reputations if score == sorted_reputations[0][1]]
    return random.choice(top_reputations)

# Run 5000 tests
trait_list = list({
    "Brave", "Cautious", "Curious", "Loyal", "Greedy", "Honest", "Deceptive", "Charismatic", "Impulsive",
    "Reserved", "Ambitious", "Lazy", "Friendly", "Temperamental", "Righteous", "Sarcastic", "Arrogant",
    "Protective", "Dreamy", "Pessimistic", "Cheerful", "Brooding", "Stoic", "Generous", "Vindictive",
    "Adventurous", "Meticulous", "Reckless", "Optimistic", "Skeptical", "Compassionate", "Calculating",
    "Patient", "Hot-headed", "Wise", "Naive", "Cynical", "Romantic", "Pragmatic", "Stubborn", "Ruthless",
    "Manipulative", "Hypercritical", "Obsessive", "Cruel", "Fanatical", "Jealous", "Crazy", "Eccentric"
})

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