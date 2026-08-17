import os
import json
import pandas as pd


# ============================================================
# NetSage AI - Evidence Checker
# ============================================================

CSV_FILE = "data/NetSage_30_Cases.csv"
EVIDENCE_FOLDER = "evidence"
RESULT_FOLDER = "results"
RESULT_FILE = os.path.join(RESULT_FOLDER, "rule_results.csv")


# ============================================================
# Utility Functions
# ============================================================

def load_json(file_path):
    """
    Load one evidence JSON file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        print(f"ERROR reading {file_path}: {error}")
        return None


def clean_value(value):
    """
    Convert a value into a clean string.
    Removes common symbols used in the evidence files.
    """

    if value is None:
        return ""

    value = str(value)

    value = value.replace("❌", "")
    value = value.replace("✅", "")
    value = value.strip()

    return value


# ============================================================
# VLAN RULES
# ============================================================

def check_vlan(case_id, structured):
    """
    Handles NET-001 to NET-005 and NET-030.
    """

    # --------------------------------------------------------
    # NET-001
    # Wrong Access VLAN
    # --------------------------------------------------------

    if case_id == "NET-001":

        actual_vlan = structured.get("actual_vlan")
        expected_vlan = structured.get("expected_vlan")

        if actual_vlan is None or expected_vlan is None:
            return (
                "NOT_CHECKED",
                "Actual VLAN and expected VLAN information is unavailable."
            )

        if actual_vlan != expected_vlan:
            return (
                "FAIL",
                f"Wrong access VLAN detected. "
                f"Actual VLAN: {actual_vlan}, "
                f"Expected VLAN: {expected_vlan}."
            )

        return "PASS", "Access VLAN is correct."

    # --------------------------------------------------------
    # NET-002
    # VLAN Not Created
    # --------------------------------------------------------

    elif case_id == "NET-002":

        required_vlan = structured.get("required_vlan")
        existing_vlans = structured.get("existing_vlans", [])

        if required_vlan is None:
            return "NOT_CHECKED", "Required VLAN information is unavailable."

        if required_vlan not in existing_vlans:
            return (
                "FAIL",
                f"Required VLAN {required_vlan} is missing."
            )

        return "PASS", f"Required VLAN {required_vlan} exists."

    # --------------------------------------------------------
    # NET-003
    # PCs in Different VLANs
    # --------------------------------------------------------

    elif case_id == "NET-003":

        vlan1 = structured.get("actual_vlan_pc0")
        vlan2 = structured.get("actual_vlan_pc1")

        if vlan1 is None or vlan2 is None:
            return (
                "NOT_CHECKED",
                "VLAN information for both PCs is unavailable."
            )

        if vlan1 != vlan2:
            return (
                "FAIL",
                f"PCs are in different VLANs. "
                f"PC0 VLAN: {vlan1}, PC1 VLAN: {vlan2}."
            )

        return "PASS", "Both PCs are in the same VLAN."

    # --------------------------------------------------------
    # NET-004
    # Port Left in Default VLAN
    # --------------------------------------------------------

    elif case_id == "NET-004":

        actual_vlan = structured.get("actual_vlan")
        expected_vlan = structured.get("expected_vlan")

        if actual_vlan is None or expected_vlan is None:
            return (
                "NOT_CHECKED",
                "Actual and expected VLAN information is unavailable."
            )

        if actual_vlan != expected_vlan:
            return (
                "FAIL",
                f"Port is assigned to the wrong VLAN. "
                f"Actual VLAN: {actual_vlan}, "
                f"Expected VLAN: {expected_vlan}."
            )

        return "PASS", "Port is assigned to the intended VLAN."

    # --------------------------------------------------------
    # NET-005
    # Inter-switch Link Not Trunking
    # --------------------------------------------------------

    elif case_id == "NET-005":

        trunk_status = structured.get("trunk_status")

        if trunk_status is None:
            return (
                "NOT_CHECKED",
                "Trunk status information is unavailable."
            )

        if str(trunk_status).lower() not in [
            "up",
            "trunk",
            "trunking",
            "on"
        ]:
            return "FAIL", "Inter-switch link is not trunking."

        return "PASS", "Inter-switch link is trunking."

    # --------------------------------------------------------
    # NET-030
    # AP Connected to Wrong VLAN
    # --------------------------------------------------------

    elif case_id == "NET-030":

        actual_vlan = structured.get("actual_vlan")
        expected_vlan = structured.get("expected_vlan")

        if actual_vlan is None or expected_vlan is None:
            return (
                "NOT_CHECKED",
                "AP VLAN information is unavailable."
            )

        if actual_vlan != expected_vlan:
            return (
                "FAIL",
                f"AP port VLAN mismatch. "
                f"Actual VLAN: {actual_vlan}, "
                f"Expected VLAN: {expected_vlan}."
            )

        return "PASS", "AP is connected to the correct VLAN."

    return "NOT_CHECKED", "No VLAN rule available."


# ============================================================
# GATEWAY RULES
# ============================================================

def check_missing_gateway(structured):
    """
    NET-006
    Checks whether the PC has a default gateway.
    """

    gateway_present = structured.get("gateway_present")

    if gateway_present is False:
        return "FAIL", "Default gateway is missing."

    if gateway_present is True:
        return "PASS", "Default gateway is present."

    return (
        "NOT_CHECKED",
        "Gateway presence information is unavailable."
    )


def check_wrong_gateway(structured, key_values):
    """
    NET-007
    Checks whether the configured gateway is incorrect.

    Example:
        Configured gateway = 192.168.10.254
        Correct router G0/0 = 192.168.10.1
    """

    actual_gateway = structured.get("gateway")

    correct_gateway = key_values.get("G0/0")

    if actual_gateway is None:
        return (
            "NOT_CHECKED",
            "Configured gateway information is unavailable."
        )

    if correct_gateway is None:
        return (
            "NOT_CHECKED",
            "Correct gateway information is unavailable."
        )

    actual_gateway = clean_value(actual_gateway)
    correct_gateway = clean_value(correct_gateway)

    if actual_gateway != correct_gateway:
        return (
            "FAIL",
            f"Wrong default gateway. "
            f"Configured: {actual_gateway}, "
            f"Expected: {correct_gateway}."
        )

    return "PASS", "Default gateway is correct."


def check_gateway_interface(structured):
    """
    NET-008
    Checks whether the router's gateway interface is down.
    """

    interface_status = structured.get("interface_status")

    if interface_status is None:
        return (
            "NOT_CHECKED",
            "Gateway interface status is unavailable."
        )

    status = clean_value(interface_status).lower()

    if status in [
        "down",
        "administratively down",
        "shutdown"
    ]:
        return (
            "FAIL",
            "Gateway interface is administratively down."
        )

    if status in [
        "up",
        "up up"
    ]:
        return "PASS", "Gateway interface is up."

    return (
        "NOT_CHECKED",
        f"Unknown gateway interface status: {interface_status}"
    )


def check_gateway_ip(structured, key_values):
    """
    NET-009
    Checks whether the PC gateway matches the router LAN IP.
    """

    router_ip = structured.get("interface_ip")

    pc_gateway = key_values.get("PC Gateway")

    if router_ip is None:
        return (
            "NOT_CHECKED",
            "Router LAN IP information is unavailable."
        )

    if pc_gateway is None:
        return (
            "NOT_CHECKED",
            "PC gateway information is unavailable."
        )

    router_ip = clean_value(router_ip)
    pc_gateway = clean_value(pc_gateway)

    if pc_gateway != router_ip:
        return (
            "FAIL",
            f"Gateway IP mismatch. "
            f"PC gateway: {pc_gateway}, "
            f"Router LAN IP: {router_ip}."
        )

    return "PASS", "PC gateway matches the router LAN IP."


# ============================================================
# DHCP RULES
# ============================================================

def check_dhcp(case_id, structured):
    """
    Handles NET-010 to NET-013.
    """

    # --------------------------------------------------------
    # NET-010
    # DHCP Pool Missing
    # --------------------------------------------------------

    if case_id == "NET-010":

        pool_exists = structured.get("pool_exists")

        if pool_exists is False:
            return "FAIL", "DHCP pool is missing."

        if pool_exists is True:
            return "PASS", "DHCP pool exists."

        return (
            "NOT_CHECKED",
            "DHCP pool information is unavailable."
        )

    # --------------------------------------------------------
    # NET-011
    # Wrong DHCP Network
    # --------------------------------------------------------

    elif case_id == "NET-011":

        actual_network = structured.get("actual_network")
        expected_network = structured.get("expected_network")

        if actual_network is None or expected_network is None:
            return (
                "NOT_CHECKED",
                "DHCP network information is unavailable."
            )

        if actual_network != expected_network:
            return (
                "FAIL",
                f"Wrong DHCP network. "
                f"Actual: {actual_network}, "
                f"Expected: {expected_network}."
            )

        return "PASS", "DHCP network is correct."

    # --------------------------------------------------------
    # NET-012
    # Wrong DHCP Default Router
    # --------------------------------------------------------

    elif case_id == "NET-012":

        actual_gateway = structured.get("actual_gateway")
        expected_gateway = structured.get("expected_gateway")

        if actual_gateway is None or expected_gateway is None:
            return (
                "NOT_CHECKED",
                "DHCP default-router information is unavailable."
            )

        if actual_gateway != expected_gateway:
            return (
                "FAIL",
                f"Wrong DHCP default-router. "
                f"Actual: {actual_gateway}, "
                f"Expected: {expected_gateway}."
            )

        return "PASS", "DHCP default-router is correct."

    # --------------------------------------------------------
    # NET-013
    # Wrong DHCP DNS
    # --------------------------------------------------------

    elif case_id == "NET-013":

        actual_dns = structured.get("actual_dns")
        expected_dns = structured.get("expected_dns")

        if actual_dns is None or expected_dns is None:
            return (
                "NOT_CHECKED",
                "DHCP DNS information is unavailable."
            )

        if actual_dns != expected_dns:
            return (
                "FAIL",
                f"Wrong DHCP DNS server. "
                f"Actual: {actual_dns}, "
                f"Expected: {expected_dns}."
            )

        return "PASS", "DHCP DNS server is correct."

    return "NOT_CHECKED", "No DHCP rule available."


# ============================================================
# DNS RULES
# ============================================================

def check_dns(case_id, structured):
    """
    Handles NET-014 to NET-016.
    """

    # NET-014
    if case_id == "NET-014":

        actual_dns = structured.get("actual_dns")
        expected_dns = structured.get("expected_dns")

        if actual_dns is None or expected_dns is None:
            return (
                "NOT_CHECKED",
                "DNS server information is unavailable."
            )

        if actual_dns != expected_dns:
            return (
                "FAIL",
                f"Wrong DNS server. "
                f"Actual: {actual_dns}, "
                f"Expected: {expected_dns}."
            )

        return "PASS", "DNS server is correct."

    # NET-015
    elif case_id == "NET-015":

        dns_enabled = structured.get("dns_enabled")

        if dns_enabled is False:
            return "FAIL", "DNS service is disabled."

        if dns_enabled is True:
            return "PASS", "DNS service is enabled."

        return (
            "NOT_CHECKED",
            "DNS service status is unavailable."
        )

    # NET-016
    elif case_id == "NET-016":

        record_exists = structured.get("record_exists")

        if record_exists is False:
            return "FAIL", "DNS record is missing."

        if record_exists is True:
            return "PASS", "DNS record exists."

        return (
            "NOT_CHECKED",
            "DNS record information is unavailable."
        )

    return "NOT_CHECKED", "No DNS rule available."


# ============================================================
# ROUTING RULES
# ============================================================

def check_routing(case_id, structured):
    """
    Handles NET-017, NET-018 and NET-020.
    """

    # NET-017
    if case_id == "NET-017":

        route_exists = structured.get("route_exists")

        if route_exists is False:
            return "FAIL", "Required static route is missing."

        if route_exists is True:
            return "PASS", "Required static route exists."

        return (
            "NOT_CHECKED",
            "Static route information is unavailable."
        )

    # NET-018
    elif case_id == "NET-018":

        actual_next_hop = structured.get("actual_next_hop")
        expected_next_hop = structured.get("expected_next_hop")

        if actual_next_hop is None or expected_next_hop is None:
            return (
                "NOT_CHECKED",
                "Next-hop information is unavailable."
            )

        if actual_next_hop != expected_next_hop:
            return (
                "FAIL",
                f"Wrong next hop. "
                f"Actual: {actual_next_hop}, "
                f"Expected: {expected_next_hop}."
            )

        return "PASS", "Next hop is correct."

    # NET-020
    elif case_id == "NET-020":

        default_route_exists = structured.get("default_route_exists")

        if default_route_exists is False:
            return "FAIL", "Default route is missing."

        if default_route_exists is True:
            return "PASS", "Default route exists."

        return (
            "NOT_CHECKED",
            "Default route information is unavailable."
        )

    return "NOT_CHECKED", "No routing rule available."


# ============================================================
# NET-019 - Router Interface Down
# ============================================================

def check_router_interface(structured):
    """
    NET-019
    Checks whether a router-to-router interface is down.
    """

    interface_status = structured.get("interface_status")

    if interface_status is None:
        return (
            "NOT_CHECKED",
            "Router interface status is unavailable."
        )

    status = clean_value(interface_status).lower()

    if status in [
        "down",
        "administratively down",
        "shutdown"
    ]:
        return (
            "FAIL",
            "Router interface is administratively down."
        )

    if status in [
        "up",
        "up up"
    ]:
        return "PASS", "Router interface is up."

    return (
        "NOT_CHECKED",
        f"Unknown router interface status: {interface_status}"
    )


# ============================================================
# ACL RULES
# ============================================================

def check_acl(case_id, structured):
    """
    Handles NET-021 to NET-023.
    """

    # NET-021
    if case_id == "NET-021":

        icmp_allowed = structured.get("icmp_allowed")

        if icmp_allowed is False:
            return "FAIL", "ACL is blocking ICMP traffic."

        if icmp_allowed is True:
            return "PASS", "ICMP traffic is allowed."

        return (
            "NOT_CHECKED",
            "ICMP ACL information is unavailable."
        )

    # NET-022
    elif case_id == "NET-022":

        http_allowed = structured.get("http_allowed")

        if http_allowed is False:
            return "FAIL", "ACL is blocking HTTP traffic."

        if http_allowed is True:
            return "PASS", "HTTP traffic is allowed."

        return (
            "NOT_CHECKED",
            "HTTP ACL information is unavailable."
        )

    # NET-023
    elif case_id == "NET-023":

        placement_correct = structured.get("placement_correct")

        if placement_correct is False:
            return "FAIL", "ACL placement is incorrect."

        if placement_correct is True:
            return "PASS", "ACL placement is correct."

        return (
            "NOT_CHECKED",
            "ACL placement information is unavailable."
        )

    return "NOT_CHECKED", "No ACL rule available."


# ============================================================
# NAT RULES
# ============================================================

def check_nat(case_id, structured):
    """
    Handles NET-024 to NET-026.
    """

    # NET-024
    if case_id == "NET-024":

        nat_exists = structured.get("nat_exists")

        if nat_exists is False:
            return "FAIL", "NAT configuration is missing."

        if nat_exists is True:
            return "PASS", "NAT configuration exists."

        return (
            "NOT_CHECKED",
            "NAT configuration information is unavailable."
        )

    # NET-025
    elif case_id == "NET-025":

        roles_correct = structured.get("roles_correct")

        if roles_correct is False:
            return "FAIL", "NAT inside/outside interface roles are incorrect."

        if roles_correct is True:
            return "PASS", "NAT interface roles are correct."

        return (
            "NOT_CHECKED",
            "NAT interface role information is unavailable."
        )

    # NET-026
    elif case_id == "NET-026":

        acl_match = structured.get("acl_match")

        if acl_match is False:
            return "FAIL", "NAT ACL mismatch detected."

        if acl_match is True:
            return "PASS", "NAT ACL matches the required configuration."

        return (
            "NOT_CHECKED",
            "NAT ACL information is unavailable."
        )

    return "NOT_CHECKED", "No NAT rule available."


# ============================================================
# WIRELESS RULES
# ============================================================

def check_wireless(case_id, structured):
    """
    Handles NET-027 to NET-029.
    """

    # NET-027
    if case_id == "NET-027":

        actual_ssid = structured.get("actual_ssid")
        expected_ssid = structured.get("expected_ssid")

        if actual_ssid is None or expected_ssid is None:
            return (
                "NOT_CHECKED",
                "SSID information is unavailable."
            )

        if actual_ssid != expected_ssid:
            return (
                "FAIL",
                f"Wrong SSID. "
                f"Actual: {actual_ssid}, "
                f"Expected: {expected_ssid}."
            )

        return "PASS", "SSID is correct."

    # NET-028
    elif case_id == "NET-028":

        password_correct = structured.get("password_correct")

        if password_correct is False:
            return "FAIL", "Wireless password is incorrect."

        if password_correct is True:
            return "PASS", "Wireless password is correct."

        return (
            "NOT_CHECKED",
            "Wireless password information is unavailable."
        )

    # NET-029
    elif case_id == "NET-029":

        network_working = structured.get("network_working")

        if network_working is False:
            return "FAIL", "Wireless client has a DHCP/network problem."

        if network_working is True:
            return "PASS", "Wireless client network configuration is working."

        return (
            "NOT_CHECKED",
            "Wireless network information is unavailable."
        )

    return "NOT_CHECKED", "No wireless rule available."


# ============================================================
# RULE IDENTIFICATION
# ============================================================

def identify_rule(case_id, category):
    """
    Selects the correct checker based on the case ID/category.
    """

    if case_id in [
        "NET-001",
        "NET-002",
        "NET-003",
        "NET-004",
        "NET-005",
        "NET-030"
    ]:
        return "VLAN Checker"

    if case_id in [
        "NET-006",
        "NET-007",
        "NET-008",
        "NET-009"
    ]:
        return "Gateway Checker"

    if case_id in [
        "NET-010",
        "NET-011",
        "NET-012",
        "NET-013"
    ]:
        return "DHCP Checker"

    if case_id in [
        "NET-014",
        "NET-015",
        "NET-016"
    ]:
        return "DNS Checker"

    if case_id in [
        "NET-017",
        "NET-018",
        "NET-020"
    ]:
        return "Route Checker"

    if case_id == "NET-019":
        return "Route Checker"

    if case_id in [
        "NET-021",
        "NET-022",
        "NET-023"
    ]:
        return "ACL Checker"

    if case_id in [
        "NET-024",
        "NET-025",
        "NET-026"
    ]:
        return "NAT Checker"

    if case_id in [
        "NET-027",
        "NET-028",
        "NET-029"
    ]:
        return "Wireless Checker"

    return "No matching rule"


# ============================================================
# RUN ONE CASE
# ============================================================

def run_case(case_id, category, evidence):
    """
    Runs the appropriate rule for one case.
    """

    structured = evidence.get("structured_evidence", {})

    key_values = evidence.get(
        "evidence",
        {}
    ).get(
        "key_value_information",
        {}
    )

    # --------------------------------------------------------
    # VLAN
    # --------------------------------------------------------

    if case_id in [
        "NET-001",
        "NET-002",
        "NET-003",
        "NET-004",
        "NET-005",
        "NET-030"
    ]:

        return check_vlan(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # Gateway
    # --------------------------------------------------------

    elif case_id == "NET-006":

        return check_missing_gateway(
            structured
        )

    elif case_id == "NET-007":

        return check_wrong_gateway(
            structured,
            key_values
        )

    elif case_id == "NET-008":

        return check_gateway_interface(
            structured
        )

    elif case_id == "NET-009":

        return check_gateway_ip(
            structured,
            key_values
        )

    # --------------------------------------------------------
    # DHCP
    # --------------------------------------------------------

    elif case_id in [
        "NET-010",
        "NET-011",
        "NET-012",
        "NET-013"
    ]:

        return check_dhcp(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # DNS
    # --------------------------------------------------------

    elif case_id in [
        "NET-014",
        "NET-015",
        "NET-016"
    ]:

        return check_dns(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # Routing
    # --------------------------------------------------------

    elif case_id in [
        "NET-017",
        "NET-018",
        "NET-020"
    ]:

        return check_routing(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # NET-019
    # --------------------------------------------------------

    elif case_id == "NET-019":

        return check_router_interface(
            structured
        )

    # --------------------------------------------------------
    # ACL
    # --------------------------------------------------------

    elif case_id in [
        "NET-021",
        "NET-022",
        "NET-023"
    ]:

        return check_acl(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # NAT
    # --------------------------------------------------------

    elif case_id in [
        "NET-024",
        "NET-025",
        "NET-026"
    ]:

        return check_nat(
            case_id,
            structured
        )

    # --------------------------------------------------------
    # Wireless
    # --------------------------------------------------------

    elif case_id in [
        "NET-027",
        "NET-028",
        "NET-029"
    ]:

        return check_wireless(
            case_id,
            structured
        )

    return (
        "NOT_CHECKED",
        "No rule implemented for this case."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==========================================")
    print("        NetSage AI Evidence Checker")
    print("==========================================")
    print()

    # --------------------------------------------------------
    # Check CSV
    # --------------------------------------------------------

    if not os.path.exists(CSV_FILE):

        print(
            f"ERROR: CSV file not found: {CSV_FILE}"
        )

        return

    # --------------------------------------------------------
    # Check evidence folder
    # --------------------------------------------------------

    if not os.path.exists(EVIDENCE_FOLDER):

        print(
            f"ERROR: Evidence folder not found: "
            f"{EVIDENCE_FOLDER}"
        )

        return

    # --------------------------------------------------------
    # Load CSV
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            CSV_FILE
        )

    except Exception as error:

        print(
            f"ERROR loading CSV: {error}"
        )

        return

    print(
        f"Loaded {len(df)} cases from CSV."
    )

    print()
    print("Reading evidence files...")
    print()

    # --------------------------------------------------------
    # Create results folder
    # --------------------------------------------------------

    os.makedirs(
        RESULT_FOLDER,
        exist_ok=True
    )

    results = []

    total_cases = 0
    evidence_found = 0
    evidence_missing = 0

    pass_count = 0
    fail_count = 0
    not_checked_count = 0

    # --------------------------------------------------------
    # Process every case
    # --------------------------------------------------------

    for _, row in df.iterrows():

        case_id = str(
            row.get("Case ID", "")
        ).strip()

        category = str(
            row.get("Category", "")
        ).strip()

        total_cases += 1

        evidence_file = os.path.join(
            EVIDENCE_FOLDER,
            f"{case_id}.json"
        )

        # ----------------------------------------------------
        # Evidence missing
        # ----------------------------------------------------

        if not os.path.exists(evidence_file):

            evidence_missing += 1

            rule = identify_rule(
                case_id,
                category
            )

            status = "NOT_CHECKED"

            finding = (
                "Evidence file is missing."
            )

            results.append({
                "Case ID": case_id,
                "Category": category,
                "Expected Fault": row.get(
                    "Expected Fault",
                    row.get(
                        "Expected Fault / Root Cause",
                        ""
                    )
                ),
                "Rule": rule,
                "Status": status,
                "Finding": finding
            })

            print(
                f"{case_id:<10} | "
                f"{rule:<28} | "
                f"{status}"
            )

            not_checked_count += 1

            continue

        # ----------------------------------------------------
        # Evidence found
        # ----------------------------------------------------

        evidence_found += 1

        evidence = load_json(
            evidence_file
        )

        if evidence is None:

            rule = identify_rule(
                case_id,
                category
            )

            status = "NOT_CHECKED"

            finding = (
                "Evidence JSON could not be loaded."
            )

        else:

            rule = identify_rule(
                case_id,
                category
            )

            status, finding = run_case(
                case_id,
                category,
                evidence
            )

        # ----------------------------------------------------
        # Count result
        # ----------------------------------------------------

        if status == "PASS":

            pass_count += 1

        elif status == "FAIL":

            fail_count += 1

        else:

            not_checked_count += 1

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({
            "Case ID": case_id,
            "Category": category,
            "Expected Fault": row.get(
                "Expected Fault",
                row.get(
                    "Expected Fault / Root Cause",
                    ""
                )
            ),
            "Rule": rule,
            "Status": status,
            "Finding": finding
        })

        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print(
            f"{case_id:<10} | "
            f"{rule:<28} | "
            f"{status}"
        )

    # ========================================================
    # Save Results
    # ========================================================

    results_df = pd.DataFrame(
        results
    )

    try:

        results_df.to_csv(
            RESULT_FILE,
            index=False
        )

    except Exception as error:

        print()
        print(
            f"ERROR saving results: {error}"
        )

        return

    # ========================================================
    # Final Summary
    # ========================================================

    print()
    print("==========================================")
    print("        Rule Checking Completed")
    print("==========================================")
    print()

    print(
        f"Total Cases       : {total_cases}"
    )

    print(
        f"Evidence Found    : {evidence_found}"
    )

    print(
        f"Evidence Missing  : {evidence_missing}"
    )

    print(
        f"PASS              : {pass_count}"
    )

    print(
        f"FAIL              : {fail_count}"
    )

    print(
        f"NOT_CHECKED       : {not_checked_count}"
    )

    print()
    print("Results saved to:")
    print(
        RESULT_FILE
    )

    print()
    print("==========================================")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()