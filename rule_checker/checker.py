import pandas as pd
import os


# ============================================================
# NETSAGE AI - RULE CHECKER
# ============================================================

CSV_FILE = "data/NetSage_30_Cases.csv"
RESULT_FILE = "results/rule_results.csv"


# ============================================================
# RULE CHECKERS
# ============================================================

def check_gateway(pc_ip, gateway):
    if not gateway or gateway == "0.0.0.0":
        return "FAIL", "Default gateway is missing."

    pc_network = ".".join(pc_ip.split(".")[:3])
    gateway_network = ".".join(gateway.split(".")[:3])

    if pc_network != gateway_network:
        return "FAIL", "Gateway mismatch detected."

    return "PASS", "Gateway appears to be correct."


def check_subnet_mask(actual_mask, expected_mask):
    if actual_mask != expected_mask:
        return "FAIL", "Wrong subnet mask detected."

    return "PASS", "Subnet mask appears to be correct."


def check_interface_status(status):
    if str(status).lower() != "up":
        return "FAIL", "Interface is down."

    return "PASS", "Interface is up."


def check_vlan(required_vlan, existing_vlans):
    if required_vlan not in existing_vlans:
        return "FAIL", "Required VLAN is missing."

    return "PASS", "Required VLAN exists."


def check_route(required_network, routing_table):
    if required_network not in routing_table:
        return "FAIL", "Required route is missing."

    return "PASS", "Required route exists."


def check_duplicate_ips(ip_addresses):
    if len(ip_addresses) != len(set(ip_addresses)):
        return "FAIL", "Duplicate IP address detected."

    return "PASS", "No duplicate IP addresses found."


# ============================================================
# RULE IDENTIFICATION
# ============================================================

def identify_rule(category, expected_fault):

    text = (
        str(category) + " " +
        str(expected_fault)
    ).lower()

    if "gateway" in text:
        return "Gateway Checker"

    elif "subnet" in text or "mask" in text:
        return "Subnet Mask Checker"

    elif "interface" in text or "shutdown" in text:
        return "Interface Status Checker"

    elif "vlan" in text:
        return "VLAN Checker"

    elif "route" in text or "routing" in text:
        return "Route Checker"

    elif "duplicate" in text:
        return "Duplicate IP Checker"

    elif "dhcp" in text:
        return "DHCP Checker"

    elif "dns" in text:
        return "DNS Checker"

    elif "acl" in text:
        return "ACL Checker"

    elif "nat" in text:
        return "NAT Checker"

    elif "ssid" in text or "wireless" in text:
        return "Wireless Checker"

    return "No matching rule"


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("======================================")
    print("        NetSage AI Rule Checker")
    print("======================================")
    print()

    # --------------------------------------------------------
    # Check CSV file
    # --------------------------------------------------------

    if not os.path.exists(CSV_FILE):
        print("ERROR: CSV file not found.")
        print("Expected location:")
        print(CSV_FILE)
        return

    # --------------------------------------------------------
    # Load CSV
    # --------------------------------------------------------

    df = pd.read_csv(CSV_FILE)

    # Remove accidental spaces from column names
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    print(f"Loaded {len(df)} cases from CSV.")
    print()

    # --------------------------------------------------------
    # Display actual column names
    # --------------------------------------------------------

    print("CSV columns detected:")

    for column in df.columns:
        print(" -", repr(column))

    print()

    # --------------------------------------------------------
    # Find expected fault column
    # --------------------------------------------------------

    fault_column = None

    possible_columns = [
        "Expected Fault",
        "Expected Fault / Root Cause",
        "Expected_Fault",
        "ExpectedFault"
    ]

    for column in possible_columns:

        if column in df.columns:
            fault_column = column
            break

    if fault_column is None:

        print("ERROR: Could not find the Expected Fault column.")

        print()
        print("Available columns are:")

        for column in df.columns:
            print(repr(column))

        return

    print("Using fault column:", fault_column)
    print()

    # --------------------------------------------------------
    # Create results
    # --------------------------------------------------------

    results = []

    for _, row in df.iterrows():

        case_id = str(row["Case ID"])
        category = str(row["Category"])
        expected_fault = str(row[fault_column])

        rule = identify_rule(
            category,
            expected_fault
        )

        # At this stage we do not have actual
        # Packet Tracer evidence automatically connected.
        status = "NOT_CHECKED"

        finding = (
            "Actual Packet Tracer evidence is required "
            "to run this rule."
        )

        results.append({
            "Case ID": case_id,
            "Category": category,
            "Expected Fault": expected_fault,
            "Rule": rule,
            "Status": status,
            "Finding": finding
        })

    # --------------------------------------------------------
    # Create results folder
    # --------------------------------------------------------

    os.makedirs("results", exist_ok=True)

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        RESULT_FILE,
        index=False
    )

    print("Rule checking completed.")
    print()
    print(f"Results saved to: {RESULT_FILE}")
    print()

    # --------------------------------------------------------
    # Display first few results
    # --------------------------------------------------------

    print("Sample results:")
    print()

    print(results_df.head(10).to_string(index=False))


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()