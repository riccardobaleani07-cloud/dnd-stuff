from collections import defaultdict
import npc_static_data.modifiers as modifiers


EXPR_OPS = {"rd_choice", "max", "min", "add", "multiply", "divide", "inverse"}
LEAF_OPS = {"const", "stat"}


# -----------------------------
# TYPE CLASSIFICATION
# -----------------------------

def classify_atom(x):
    if isinstance(x, bool):
        return "bool"
    if isinstance(x, (int, float)):
        return "number"
    if isinstance(x, str):
        return "string"
    if isinstance(x, tuple):
        return "tuple"
    if isinstance(x, list):
        return "list"
    if isinstance(x, dict):
        return "expr"
    return type(x).__name__


# -----------------------------
# OP DETECTION
# -----------------------------

def get_expr_type(d):
    for k in d.keys():
        if k in EXPR_OPS:
            return k
    return None


def get_leaf_type(d):
    for k in d.keys():
        if k in LEAF_OPS:
            return k
    return None


def is_expr_dict(d):
    return isinstance(d, dict) and (
        any(k in EXPR_OPS for k in d.keys()) or
        any(k in LEAF_OPS for k in d.keys())
    )


# -----------------------------
# STATS INIT
# -----------------------------

def make_stats_entry():
    return {
        "atomic_count": 0,
        "list_count": 0,

        "atomic_types": defaultdict(int),
        "list_atoms": defaultdict(int),

        # NEW: leaf expressions
        "leaf_types": defaultdict(int),

        # operator patterns
        "patterns": defaultdict(int)
    }


# -----------------------------
# RECURSION
# -----------------------------

def analyze_expression(expr, stats):

    if not is_expr_dict(expr):
        return

    op = get_expr_type(expr)
    leaf = get_leaf_type(expr)
    operand = next(iter(expr.values()))

    entry = stats[op] if op else stats["UNKNOWN"]

    # -------------------------
    # LEAF EXPRESSIONS (FIX)
    # -------------------------
    if leaf is not None:
        entry["leaf_types"][leaf] += 1
        return  # IMPORTANT: leaf has no operands to recurse

    # -------------------------
    # OPERATOR EXPRESSIONS
    # -------------------------
    if op is None:
        return

    # -------------------------
    # LIST OPERAND
    # -------------------------
    if isinstance(operand, list):

        entry["list_count"] += 1

        pattern = []

        for x in operand:

            if is_expr_dict(x):

                nested_op = get_expr_type(x) or get_leaf_type(x) or "UNKNOWN"

                entry["list_atoms"][f"expr:{nested_op}"] += 1
                pattern.append(f"expr:{nested_op}")

                analyze_expression(x, stats)

            else:
                t = classify_atom(x)
                entry["list_atoms"][t] += 1
                pattern.append(t)

        entry["patterns"][tuple(pattern)] += 1

    # -------------------------
    # ATOMIC OPERAND
    # -------------------------
    else:

        entry["atomic_count"] += 1

        if is_expr_dict(operand):

            nested = get_expr_type(operand) or get_leaf_type(operand) or "UNKNOWN"
            entry["atomic_types"][f"expr:{nested}"] += 1

            analyze_expression(operand, stats)

        else:
            t = classify_atom(operand)
            entry["atomic_types"][t] += 1


# -----------------------------
# EXPRESSION LIST HANDLER
# -----------------------------

def analyze_expr_list(expr_list, stats):
    if isinstance(expr_list, list):
        for expr in expr_list:
            analyze_expression(expr, stats)


# -----------------------------
# FIND ALL EXPR LISTS
# -----------------------------

def find_expr_nodes(node, out):

    if isinstance(node, dict):

        if "expr" in node:
            out.append(node["expr"])

        for v in node.values():
            find_expr_nodes(v, out)

    elif isinstance(node, list):

        for v in node:
            find_expr_nodes(v, out)


# -----------------------------
# MAIN
# -----------------------------

def scan_dataset(root):

    expr_nodes = []
    find_expr_nodes(root, expr_nodes)

    stats = defaultdict(make_stats_entry)

    for expr_list in expr_nodes:
        analyze_expr_list(expr_list, stats)

    return stats


# -----------------------------
# RUN
# -----------------------------

all_data = {
    "race": modifiers.race,
    "subtype": modifiers.subtype,
    "age_category": modifiers.age_category,
    "jobs": modifiers.jobs
}

stats = scan_dataset(all_data)

print("\n--- RESULTS ---\n")

for op, data in stats.items():
    print(f"OP: {op}")

    print("  atomic_count:", data["atomic_count"])
    for k, v in data["atomic_types"].items():
        print("   ", k, v)

    print("  list_count:", data["list_count"])
    for k, v in data["list_atoms"].items():
        print("   ", k, v)

    print("  leaf expressions:")
    for k, v in data["leaf_types"].items():
        print("   ", k, v)

    print("  patterns:")
    for pattern, count in sorted(data["patterns"].items(), key=lambda x: x[1], reverse=True):
        print("    ", list(pattern), "->", count)

    print()