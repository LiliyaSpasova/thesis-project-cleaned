# Важен коментар!
# Run this only after running
# pipreqs . --force

import yaml

# Read dependencies from requirements.txt
with open("requirements.txt", "r") as file:
    dependencies = [line.strip() for line in file if line.strip()]

# Create YAML structure
yaml_data = {
    "dependencies": dependencies
}

# Write to dependencies.yaml
with open("dependencies.yaml", "w") as file:
    yaml.dump(yaml_data, file, default_flow_style=False)

print("dependencies.yaml created successfully!")
