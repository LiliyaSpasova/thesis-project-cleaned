import os
from collections import defaultdict

# Step 1: Read and filter entries with evidence
entries_with_evidence = []
with open("filtered_results/high.txt", "r") as f:
    block = {}
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Target:"):
            target_line = line.replace("Target:", "").strip()
            if "Given:" not in target_line:
                block = {}  # Skip this block if no evidence
                continue
            block["target"] = target_line
            # Extract the evidence part for grouping
            evidence_part = target_line.split("Given:")[-1].strip()
            block["evidence"] = evidence_part
        elif line.startswith("Param1:"):
            block["param1"] = line.replace("Param1:", "").strip()
        elif line.startswith("Param2:"):
            block["param2"] = line.replace("Param2:", "").strip()
        elif line.startswith("Value:"):
            block["value"] = line.replace("Value:", "").strip()
        elif line == "---":
            if all(key in block for key in ["target", "param1", "param2", "value", "evidence"]):
                entries_with_evidence.append(block)
            block = {}

# Step 2: Group by evidence
grouped_by_evidence = defaultdict(list)
for entry in entries_with_evidence:
    grouped_by_evidence[entry["evidence"]].append(entry)

# Step 3: Write each group to a separate file
output_dir = "split_outputs_high_with_evidence"
os.makedirs(output_dir, exist_ok=True)

for evidence, group in grouped_by_evidence.items():
    # Clean filename (remove or replace unsafe characters)
    safe_evidence = evidence.replace(" ", "_").replace("|", "").replace("=", "").replace("(", "").replace(")", "").replace("-", "")
    filename = f"{output_dir}/evidence__{safe_evidence}.txt"

    with open(filename, "w") as f:
        for entry in group:
            f.write(f"Target: {entry['target']}\n")
            f.write(f"Param1: {entry['param1']}\n")
            f.write(f"Param2: {entry['param2']}\n")
            f.write(f"Value: {entry['value']}\n")
            f.write("---\n")

print(f"Done! {len(grouped_by_evidence)} groups with evidence saved in '{output_dir}'")
