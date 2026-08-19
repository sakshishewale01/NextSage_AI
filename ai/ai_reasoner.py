import os
import json
import pandas as pd


# ============================================================
# NetSage AI - AI Reasoning Layer
# ============================================================

RULE_RESULTS_FILE = "results/rule_results.csv"
EVIDENCE_FOLDER = "evidence"
OUTPUT_FILE = "results/ai_diagnosis_results.csv"
PROMPT_FILE = "prompts/diagnose_prompt.md"


# ============================================================
# Load Prompt
# ============================================================

def load_prompt():

    if not os.path.exists(PROMPT_FILE):
        return ""

    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        return file.read()


# ============================================================
# Load Evidence
# ============================================================

def load_evidence(case_id):

    file_path = os.path.join(
        EVIDENCE_FOLDER,
        f"{case_id}.json"
    )

    if not os.path.exists(file_path):
        return {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"Warning: Could not read {file_path}: {error}"
        )

        return {}


# ============================================================
# AI-style Reasoning
# ============================================================

def reason_about_case(row, evidence):

    case_id = str(row["Case ID"])
    category = str(row["Category"])
    status = str(row["Status"])
    finding = str(row["Finding"])

    structured = evidence.get(
        "structured_evidence",
        {}
    )

    root_cause = evidence.get(
        "root_cause",
        ""
    )

    solution = evidence.get(
        "solution",
        ""
    )

    actual_evidence = evidence.get(
        "actual_evidence",
        ""
    )

    # --------------------------------------------------------
    # NET-006
    # --------------------------------------------------------

    if case_id == "NET-006":

        gateway = structured.get(
            "gateway",
            ""
        )

        diagnosis = "Missing default gateway"

        explanation = (
            f"The PC does not have a valid default gateway. "
            f"The evidence shows gateway value '{gateway}'. "
            "Without a valid gateway, the PC cannot forward "
            "traffic to remote networks."
        )

        recommended_solution = (
            "Configure the PC with the router's LAN interface "
            "IP address as its default gateway."
        )

        confidence = "HIGH"

    # --------------------------------------------------------
    # NET-007
    # --------------------------------------------------------

    elif case_id == "NET-007":

        gateway = structured.get(
            "gateway",
            ""
        )

        diagnosis = "Wrong default gateway"

        explanation = (
            f"The PC is configured with default gateway "
            f"{gateway}, but the evidence indicates that the "
            "router LAN interface uses a different address."
        )

        recommended_solution = (
            "Change the PC's default gateway to the correct "
            "router LAN interface address."
        )

        confidence = "HIGH"

    # --------------------------------------------------------
    # NET-008
    # --------------------------------------------------------

    elif case_id == "NET-008":

        interface_status = structured.get(
            "interface_status",
            ""
        )

        diagnosis = "Gateway interface is down"

        explanation = (
            "The router's LAN interface is administratively "
            "down. Therefore, the PC cannot communicate with "
            "its default gateway."
        )

        recommended_solution = (
            "Enter the affected router interface and use "
            "'no shutdown' to enable it."
        )

        confidence = "HIGH"

    # --------------------------------------------------------
    # NET-009
    # --------------------------------------------------------

    elif case_id == "NET-009":

        interface_ip = structured.get(
            "interface_ip",
            ""
        )

        diagnosis = "Gateway IP mismatch"

        explanation = (
            f"The router LAN interface is using "
            f"{interface_ip}, while the PC's configured "
            "gateway is different. Therefore, the PC cannot "
            "correctly reach its gateway."
        )

        recommended_solution = (
            f"Configure the PC's default gateway as "
            f"{interface_ip}."
        )

        confidence = "HIGH"

    # --------------------------------------------------------
    # NET-019
    # --------------------------------------------------------

    elif case_id == "NET-019":

        interface_status = structured.get(
            "interface_status",
            ""
        )

        diagnosis = "Router interface is administratively down"

        explanation = (
            "The evidence indicates that the router interface "
            "connecting the routed link is administratively down. "
            "This prevents communication between the routers."
        )

        recommended_solution = (
            "Enter the affected router interface and use "
            "'no shutdown' to restore the interface."
        )

        confidence = "HIGH"

    # --------------------------------------------------------
    # Other cases
    # --------------------------------------------------------

    else:

        diagnosis = str(
            row["Expected Fault"]
        )

        explanation = (
            "The rule checker identified this networking "
            "condition. The evidence should be reviewed to "
            "confirm the exact configuration causing the fault."
        )

        recommended_solution = (
            solution
            if solution
            else "Review the network configuration and correct "
                 "the identified fault."
        )

        confidence = (
            "HIGH"
            if status == "FAIL"
            else "MEDIUM"
        )

    return {
        "Case ID": case_id,
        "Category": category,
        "Status": status,
        "Finding": finding,
        "Diagnosis": diagnosis,
        "Root Cause": root_cause,
        "Evidence": actual_evidence,
        "Explanation": explanation,
        "Recommended Solution": recommended_solution,
        "Confidence": confidence
    }


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("==========================================")
    print("          NetSage AI Reasoner")
    print("==========================================")
    print()

    # --------------------------------------------------------
    # Check rule results
    # --------------------------------------------------------

    if not os.path.exists(RULE_RESULTS_FILE):

        print(
            "ERROR: rule_results.csv not found."
        )

        print(
            "Run checker.py first."
        )

        return

    # --------------------------------------------------------
    # Load rule results
    # --------------------------------------------------------

    df = pd.read_csv(
        RULE_RESULTS_FILE
    )

    print(
        f"Loaded {len(df)} cases."
    )

    print()

    # --------------------------------------------------------
    # Load prompt
    # --------------------------------------------------------

    prompt = load_prompt()

    if prompt:

        print(
            "Diagnostic prompt loaded."
        )

    else:

        print(
            "Warning: Diagnostic prompt not found."
        )

    print()

    # --------------------------------------------------------
    # Process cases
    # --------------------------------------------------------

    results = []

    for _, row in df.iterrows():

        case_id = str(
            row["Case ID"]
        )

        print(
            f"Analyzing {case_id}..."
        )

        evidence = load_evidence(
            case_id
        )

        result = reason_about_case(
            row,
            evidence
        )

        results.append(
            result
        )

    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    os.makedirs(
        "results",
        exist_ok=True
    )

    result_df = pd.DataFrame(
        results
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("==========================================")
    print("       AI Reasoning Completed")
    print("==========================================")
    print()

    print(
        f"Total Cases Analyzed : {len(result_df)}"
    )

    print()
    print(
        "Output saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()
    print("==========================================")


if __name__ == "__main__":
    main()