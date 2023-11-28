# -*- coding: utf-8 -*-
"""Batch grader for course assignments."""
import argparse
import glob
import json
import os

from .grader import AutomatedGrader


def main(filepath: str = None, output_folder: str = "out", potential_points: int = 100):
    """Grade an assignment."""
    graded = 0
    if filepath is None:
        print("""usage: grade_assignment.py [-h] filepath""")

    OUTPUT_FILE_PATH = os.path.join(filepath, output_folder)
    if not os.path.exists(OUTPUT_FILE_PATH):
        os.makedirs(OUTPUT_FILE_PATH)

    assignments = glob.glob(os.path.join(filepath, "*.json"))
    for assignment_filename in assignments:
        with open(assignment_filename, "r", encoding="utf-8") as f:
            try:
                assignment = json.load(f)
            except json.JSONDecodeError:
                print(f"warning: invalid JSON in assignment_filename: {assignment_filename}")
                assignment = f.read()
        grader = AutomatedGrader(assignment, potential_points=potential_points)
        grade = grader.grade()
        with open(
            os.path.join(OUTPUT_FILE_PATH, f"{os.path.basename(assignment_filename)}"), "w", encoding="utf-8"
        ) as f:
            json.dump(grade, f, indent=4)
            graded += 1

    print(f"done! Graded {graded} assignments. Output files are in {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grade a set of homework assignments.")
    parser.add_argument("filepath", type=str, help="The path to the homework files to grade.")
    parser.add_argument(
        "output_folder",
        type=str,
        nargs="?",  # optional
        default="out",
        help="The name of the subfolder where graded assignments will be saved.",
    )
    parser.add_argument(
        "potential_points",
        type=int,
        nargs="?",  # optional
        default=100,
        help="The aggregate point potential for the assignment.",
    )

    args = parser.parse_args()

    main(args.filepath, args.output_folder, args.potential_points)
