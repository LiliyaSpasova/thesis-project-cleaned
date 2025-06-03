import os
from collections import defaultdict

# Step 1: Read and filter entries
entries = []
with open("filtered_results/high.txt", "r") as f:
    block = {}
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Target:"):
            target_line = line.replace("Target:", "").strip()
            if "Given:" in target_line:
                block = {}  # Discard this block entirely
                continue
            block["target"] = target_line
        elif line.startswith("Param1:"):
            block["param1"] = line.replace("Param1:", "").strip()
        elif line.startswith("Param2:"):
            block["param2"] = line.replace("Param2:", "").strip()
        elif line.startswith("Value:"):
            block["value"] = line.replace("Value:", "").strip()
        elif line == "---":
            if all(key in block for key in ["target", "param1", "param2", "value"]):
                entries.append(block)
            block = {}

# Step 2: Group by (param1, param2)
grouped = defaultdict(list)
for entry in entries:
    key = (entry["param1"], entry["param2"])
    grouped[key].append(entry)

# Step 3: Write each group to a separate file
output_dir = "split_outputs_high_no_evidence"
os.makedirs(output_dir, exist_ok=True)

for (param1, param2), group in grouped.items():
    # Clean filenames (remove unsafe characters)
    safe_param1 = param1.replace(" ", "_").replace("|", "").replace("=", "").replace("(", "").replace(")", "").replace("-", "")
    safe_param2 = param2.replace(" ", "_").replace("|", "").replace("=", "").replace("(", "").replace(")", "").replace("-", "")
    filename = f"{output_dir}/{safe_param1}__{safe_param2}.txt"

    with open(filename, "w") as f:
        for entry in group:
            f.write(f"Target: {entry['target']}\n")
            f.write(f"Param1: {entry['param1']}\n")
            f.write(f"Param2: {entry['param2']}\n")
            f.write(f"Value: {entry['value']}\n")
            f.write("---\n")

print(f"Done! {len(grouped)} groups without evidence saved in '{output_dir}'")
