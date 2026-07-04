from npc_generation.NPC_generator_yay import NPCGenerator
from npc_static_data import modifiers

gen = NPCGenerator()


def walk(node, path="root"):
    if isinstance(node, dict):

        # Found an expression
        if "expr" in node:
            try:
                result = gen.evaluate(node["expr"])
                print(f"{path}: {result}")
            except Exception as e:
                print(f"{path}: ERROR -> {e}")

        for key, value in node.items():
            walk(value, f"{path}.{key}")

    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk(value, f"{path}[{i}]")


# Iterate through every top-level dataset
for name, value in vars(modifiers).items():

    # Skip Python internals
    if name.startswith("__"):
        continue

    # Only process dictionaries (race, jobs, age_category, ...)
    if isinstance(value, dict) & (name == "debugger"):

        print(f"\n=== Testing {name} ===")
        walk(value, name)
        print(f"=== Finished testing {name} ===\n")