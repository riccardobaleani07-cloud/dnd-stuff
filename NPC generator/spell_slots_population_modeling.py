import random
from collections import defaultdict, Counter

def clamp(x):
    return max(x, 0)

def choice(options):
    return random.choice(options)

def apply_tier(value, tier):
    """
    Simulates your tier logic.
    value can be float (important for division propagation).
    """

    # Tier 1 special seed is handled outside

    # Define behavior zones
    if tier == 1:
        return choice([3, 4, 4, 5])

    # Tier 2–4: mixed behavior
    if 2 <= tier <= 4:
        options = [
            clamp(value - 1)
        ]

        if tier == 2:
            options.append(value - 2)

        # slight carry only in mid tiers
        if tier <= 3:
            options.append(value)
            options.append(value / 2)

        return choice(options)

    # Tier 5–6: forced compression (no stability)
    if 5 <= tier <= 6:
        options = [
            clamp(value - 1),
            value / 2
        ]
        return choice(options)

    # Tier 7–9: stabilization / decay phase
    if 7 <= tier <= 9:
        options = [
            value,
            value / 2
        ]

        # Still heavy decay on the first step
        if tier == 7:
            options.append(clamp(value-1))

        return choice(options)

    return value


def generate_spell_slots():
    slots = {}
    slots[1] = apply_tier(None, 1)

    # propagate
    for tier in range(2, 10):
        slots[tier] = apply_tier(slots[tier - 1], tier)

    # final rounding (your rule)
    for k in slots:
        slots[k] = round(slots[k])

    return slots


def simulate(n=100000):
    distribution = defaultdict(Counter)

    for _ in range(n):
        result = generate_spell_slots()

        for tier, value in result.items():
            distribution[tier][value] += 1

    return distribution


def print_distribution(dist, label):
    print(f"\n===== {label} =====")
    for tier in sorted(dist.keys()):
        total = sum(dist[tier].values())
        print(f"\nTier {tier}")
        for k in sorted(dist[tier].keys()):
            print(f"  {k}: {dist[tier][k] / total:.2%}")


if __name__ == "__main__":
    runs = 1000000

    dist_with = simulate(runs)

    print_distribution(dist_with, "WITH n-1")