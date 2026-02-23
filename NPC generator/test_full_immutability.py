# test_full_immutability.py

import copy
import json
import csv
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
# Helper function for matrixes in csv files
def snapshot_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[:] for row in reader]  # copy each row
# Helper function for json files
def snapshot_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return copy.deepcopy(json.load(f))


#--------------------------------------------
matrix_path = "NPC generator/npc_static_data/languages_matrix.csv"
json_path = "NPC generator/npc_static_data/names_transition.json"

print("Taking snapshots...")
# Take initial snapshots
before = snapshot_data(data)
print("✅ data.py snapshot taken!")

before_matrix = snapshot_csv(matrix_path)
print("✅ languages_matrix.csv snapshot taken!")

before_json = snapshot_json(json_path)
print("✅ language.json snapshot taken!")
#--------------------------------------------
# Run NPC generation to see if it mutates any used data
#--------------------------------------------
print("Generating 100 NPCs...")
# Generate 100 NPCs
gen = NPCGenerator()
for _ in range(100):
    gen.generate_npc()
print("✅ Done!")
#--------------------------------------------
# Take snapshot after generation
#--------------------------------------------
print("Taking snapshots again...")
# Take final snapshots
after = snapshot_data(data)
print("✅ data.py snapshot taken!")

after_matrix = snapshot_csv(matrix_path)
print("✅ languages_matrix.csv snapshot taken!")

after_json = snapshot_json(json_path)
print("✅ language.json snapshot taken!")
#--------------------------------------------

#--------------------------------------------
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
#--------------------------------------------

#--------------------------------------------
print("data.py immutability test RUNNING...")
# Compare
for key in before:
    if not deep_compare(before[key], after[key], path=key):
        raise AssertionError(f"❌ Data mutated in attribute: {key}")

print("✅ data.py immutability test PASSED!")
#--------------------
print("languages_matrix.csv immutability test RUNNING...")
# Compare
if not deep_compare(before_matrix, after_matrix, path="languages_matrix"):
    raise AssertionError("❌ languages_matrix.csv was mutated!")
print("✅ languages_matrix.csv immutability test PASSED!")
#--------------------
print("names_transition.json immutability test RUNNING...")
# Compare
if not deep_compare(before_json, after_json, path="names_transition_json"):
    raise AssertionError("❌ names_transition.json was mutated!")
print("✅ names_transition.json immutability test PASSED!")
#--------------------
print("✅ Full data immutability test PASSED!")