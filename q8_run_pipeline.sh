
#!/bin/bash
chmod +x q8_run_pipeline.sh
# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

# NOTE: This script assumes Q1 has already been run to create directories and generate the dataset
# NOTE: Q2 (q2_process_metadata.py) is a standalone Python fundamentals exercise, not part of the main pipeline
# NOTE: Q3 (q3_data_utils.py) is a library imported by the notebooks, not run directly
# NOTE: The main pipeline runs Q4-Q7 notebooks in order

echo "Starting clinical trial data pipeline..." > reports/pipeline_log.txt

# TODO: Run analysis notebooks in order (q4-q7) using nbconvert with error handling
# Use either `$?` or `||` operator to check exit codes and stop on failure
# Add a log entry for each notebook execution or failure
# jupyter nbconvert --execute --to notebook q4_exploration.ipynb
echo "Pipeline complete!" >> reports/pipeline_log.txt

# Function to run notebooks and handle errors
run_notebook() {
    notebook="$1"
    echo "Running $notebook..." | tee -a reports/pipeline_log.txt

    # Execute notebook and output result file
    jupyter nbconvert --to notebook --execute "$notebook" --output "executed_${notebook}" >> reports/pipeline_log.txt 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Successfully executed $notebook" | tee -a reports/pipeline_log.txt
    else
        echo "❌ ERROR: Failed to execute $notebook" | tee -a reports/pipeline_log.txt
        echo "Pipeline aborted due to error in $notebook." | tee -a reports/pipeline_log.txt
        exit 1
    fi
}

# Run notebooks in order (Q4 → Q7)
run_notebook "q4_exploration.ipynb"
run_notebook "q5_missing_data.ipynb"
run_notebook "q6_transformation.ipynb"
run_notebook "q7_aggregation.ipynb"

# Completion message
echo "🎉 Pipeline complete!" | tee -a reports/pipeline_log.txt












