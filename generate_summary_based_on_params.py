import os

split_folder = "split_outputs_mid"
summary_lines = []

# Loop over each file in the split folder
for filename in os.listdir(split_folder):
    filepath = os.path.join(split_folder, filename)
    if not filename.endswith(".txt"):
        continue

    with open(filepath, "r") as f:
        content = f.read()

    # Count how many times 'Target:' appears (1 per entry)
    count = content.count("Target:")
    summary_lines.append(f"{filename}: {count} entries")

# Write the summary to a file
with open("summary_mid.txt", "w") as summary_file:
    summary_file.write("\n".join(summary_lines))

print("Summary file created: summary.txt")
