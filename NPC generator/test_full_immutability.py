# test_full_immutability.py

import copy
from npc_static_data import data
from npc_generation.NPC_generator_yay import NPCGenerator


def snapshot_data(module):
    
    #Create a deep snapshot of all public attributes
    #inside the data module.
    
    snapshot = {}
    for name in dir(module):
        if name.startswith("__"):
            continue
        value = getattr(module, name)

        # Skip callables (functions, classes)
        if callable(value):
            continue

        snapshot[name] = copy.deepcopy(value)

    return snapshot


# Take initial snapshot
before = snapshot_data(data)

# Generate 100 NPCs
gen = NPCGenerator()
for _ in range(100):
    gen.generate_npc()

# Take snapshot after generation
after = snapshot_data(data)


def deep_compare(a, b, path="root"):
    if type(a) != type(b):
        print(f"Type changed at {path}: {type(a)} -> {type(b)}")
        return False

    if isinstance(a, dict):
        for key in set(a.keys()).union(b.keys()):
            if key not in a:
                print(f"Key added at {path}: {key}")
                return False
            if key not in b:
                print(f"Key removed at {path}: {key}")
                return False
            if not deep_compare(a[key], b[key], f"{path}.{key}"):
                return False
        return True

    if isinstance(a, (list, tuple)):
        if len(a) != len(b):
            print(f"Length changed at {path}: {len(a)} -> {len(b)}")
            return False
        for i, (x, y) in enumerate(zip(a, b)):
            if not deep_compare(x, y, f"{path}[{i}]"):
                return False
        return True

    if a != b:
        print(f"Value changed at {path}: {a} -> {b}")
        return False

    return True


# Compare
for key in before:
    if not deep_compare(before[key], after[key], path=key):
        raise AssertionError(f"❌ Data mutated in attribute: {key}")

print("✅ Full data immutability test PASSED!")