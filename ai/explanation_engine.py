import pandas as pd
import os


INPUT_FILE = "results/diagnosis_results.csv"
OUTPUT_FILE = "results/explanation_results.csv"


def generate_explanation(row):

    case_id = row["Case ID"]
    status = row["Status"]
    finding = row["Finding"]

    if status == "PASS":
        explanation = (
            f"{case_id}: The network configuration was checked successfully. "
            f"No problem was detected for this case."
        )

    elif status == "FAIL":
        explanation = (
            f"{case_id}: A network problem was detected. "
            f"Finding: {finding}. "
            f"The configuration should be corrected according to the identified fault."
        )

    else:
        explanation = (
            f"{case_id}: The system could not completely verify this case. "
            f"Additional evidence or configuration information is required."
        )

    return explanation


def main():

    print()
    print("==========================================")
    print("       NetSage AI Explanation Engine")
    print("==========================================")
    print()

    # Check input file
    if not os.path.exists(INPUT_FILE):

        print(
            f"ERROR: Diagnosis file not found: {INPUT_FILE}"
        )

        print()
        print(
            "First run diagnosis_engine.py"
        )

        return

    # Read diagnosis results
    df = pd.read_csv(INPUT_FILE)

    print(
        f"Loaded {len(df)} diagnosis results."
    )

    print()
    print("Generating explanations...")
    print()

    # Generate explanation for every case
    df["Explanation"] = df.apply(
        generate_explanation,
        axis=1
    )

    # Select useful columns
    result = df[
        [
            "Case ID",
            "Status",
            "Finding",
            "Explanation"
        ]
    ]

    # Save result
    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "Explanation generation completed."
    )

    print()
    print(
        f"Total cases : {len(result)}"
    )

    print(
        f"Saved to    : {OUTPUT_FILE}"
    )

    print()
    print("==========================================")
    print("       Process Completed")
    print("==========================================")


if __name__ == "__main__":
    main()