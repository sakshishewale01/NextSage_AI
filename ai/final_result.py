import pandas as pd
import os


RULE_FILE = "results/rule_results.csv"
DIAGNOSIS_FILE = "results/diagnosis_results.csv"
EXPLANATION_FILE = "results/explanation_results.csv"

OUTPUT_FILE = "results/final_diagnosis.csv"


def main():

    print()
    print("==========================================")
    print("        NetSage AI Final Result")
    print("==========================================")
    print()

    # Check files
    for file in [RULE_FILE, DIAGNOSIS_FILE, EXPLANATION_FILE]:

        if not os.path.exists(file):
            print(f"ERROR: File not found: {file}")
            return

    # Read files
    rules = pd.read_csv(RULE_FILE)
    diagnosis = pd.read_csv(DIAGNOSIS_FILE)
    explanations = pd.read_csv(EXPLANATION_FILE)

    print("Files loaded successfully.")

    # Merge rule results with diagnosis
    final = rules.merge(
        diagnosis,
        on="Case ID",
        how="left",
        suffixes=("", "_diagnosis")
    )

    # Merge explanation
    final = final.merge(
        explanations,
        on="Case ID",
        how="left",
        suffixes=("", "_explanation")
    )

    # Save
    final.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Final diagnosis created successfully.")
    print()
    print(f"Total Cases : {len(final)}")
    print()
    print(f"Saved to: {OUTPUT_FILE}")
    print()

    print("==========================================")
    print("        Process Completed")
    print("==========================================")


if __name__ == "__main__":
    main()