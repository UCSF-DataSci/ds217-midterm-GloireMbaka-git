#!/usr/bin/env python3
"""Assignment 5, Question 2: Python Data Processing
Process configuration files for data generation.
"""

from typing import Dict
import os
import random
import statistics
import sys


def parse_config(filepath: str) -> dict:
    """Parse Key = value config file into dictionary"""
    config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments or empty lines
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: Config file '{filepath}' not found.")
        sys.exit(1)
    return config


def validate_config(config: dict) -> dict:
    """Validate configuration values using if/elif/else logic

    Returns a dict mapping config keys to boolean validity
    """
    results = {}

    try:
        rows = int(config.get("sample_data_rows", 0))
        results["sample_data_rows"] = rows > 0
    except (ValueError, TypeError):
        results["sample_data_rows"] = False

    try:
        min_val = int(config.get("sample_data_min", 0))
        results["sample_data_min"] = min_val >= 1
    except (ValueError, TypeError):
        results["sample_data_min"] = False

    try:
        max_val = int(config.get("sample_data_max", 0))
        # max must be greater than min
        results["sample_data_max"] = max_val > int(config.get("sample_data_min", 0))
    except (ValueError, TypeError):
        results["sample_data_max"] = False

    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """Generate CSV (one number per line) file with random numbers using config parameters"""
    rows = int(config["sample_data_rows"])
    min_val = int(config["sample_data_min"])
    max_val = int(config["sample_data_max"])

    dirpath = os.path.dirname(filename)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(filename, 'w') as f:
        for _ in range(rows):
            num = random.randint(min_val, max_val)
            f.write(f"{num}\n")


def calculate_statistics(data: list) -> dict:
    """Calculate basic statistics"""
    stats = {}
    if not data:
        return {"mean": None, "median": None, "sum": 0, "count": 0}

    stats["count"] = len(data)
    stats["sum"] = sum(data)
    stats["mean"] = round(statistics.mean(data), 2)
    stats["median"] = statistics.median(data)
    return stats


if __name__ == '__main__':
    config_file = "q2_config.txt"
    data_file = "data/sample_data.csv"
    stats_file = "output/statistics.txt"

    # Step 1: Parse config
    config = parse_config(config_file)

    # Step 2: Validate config
    validation = validate_config(config)
    if not all(validation.values()):
        print("Error: Invalid configuration values detected:")
        for k, v in validation.items():
            if not v:
                print(f"  - {k} is invalid")
        sys.exit(1)

    # Step 3: Generate sample data
    generate_sample_data(data_file, config)

    # Step 4: Read generated data
    with open(data_file, 'r') as f:
        data = [int(line.strip()) for line in f if line.strip()]

    # Step 5: Calculate statistics
    stats = calculate_statistics(data)

    # Step 6: Save statistics
    stats_dir = os.path.dirname(stats_file)
    if stats_dir:
        os.makedirs(stats_dir, exist_ok=True)
    with open(stats_file, 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    print("✅ Data generation complete.")
    print(f"- Sample data saved to: {data_file}")
    print(f"- Statistics saved to: {stats_file}")

