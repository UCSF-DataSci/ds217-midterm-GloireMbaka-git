# TODO: Add shebang line: #!/bin/bash
# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project
# TODO: Make this script executable (if not already)
chmod +x q1_setup_project.sh

# TODO: Create the following directories:
#!/bin/bash
#   - data/
mkdir -p data

#   - output/
mkdir -p output

#   - reports/
mkdir -p reports


# TODO: Generate the dataset
#       Run: python3 generate_data.py
python3 generate_data.py
#       This creates data/clinical_trial_raw.csv with 10,000 patients

# TODO: Save the directory structure to reports/directory_structure.txt
#       Hint: Use 'ls -la' or 'tree' command

ls -la

# Save directory structure with tree
tree -a > reports/directory_structure.txt


