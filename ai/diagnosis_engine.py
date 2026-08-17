import os
import pandas as pd


# ============================================================
# NetSage AI - Diagnosis Engine
# ============================================================

RULE_RESULTS_FILE = "results/rule_results.csv"
OUTPUT_FILE = "results/diagnosis_results.csv"


# ============================================================
# Diagnosis Rules
# ============================================================

def generate_diagnosis(row):

    case_id = str(row["Case ID"])
    category = str(row["Category"])
    fault = str(row["Expected Fault"])
    status = str(row["Status"])
    finding = str(row["Finding"])

    # --------------------------------------------------------
    # NET-001 to NET-005 : VLAN
    # --------------------------------------------------------

    if case_id == "NET-001":
        diagnosis = "Wrong access VLAN"
        explanation = (
            "The switch port is assigned to an incorrect VLAN. "
            "The PC should be connected to the required VLAN."
        )
        solution = (
            "Configure the affected switch port as an access port "
            "and assign it to the correct VLAN."
        )

    elif case_id == "NET-002":
        diagnosis = "Required VLAN missing"
        explanation = (
            "The required VLAN does not exist on the switch."
        )
        solution = (
            "Create the required VLAN and assign the appropriate "
            "switch ports to it."
        )

    elif case_id == "NET-003":
        diagnosis = "Ports are in different VLANs"
        explanation = (
            "The connected devices are placed in different VLANs, "
            "preventing normal Layer-2 communication."
        )
        solution = (
            "Assign the relevant switch ports to the same VLAN."
        )

    elif case_id == "NET-004":
        diagnosis = "Port assigned to wrong VLAN"
        explanation = (
            "The affected switch port is not assigned to the "
            "intended VLAN."
        )
        solution = (
            "Change the switch port configuration and assign it "
            "to the intended VLAN."
        )

    elif case_id == "NET-005":
        diagnosis = "Inter-switch link is not trunking"
        explanation = (
            "The link between switches is not correctly configured "
            "as a trunk."
        )
        solution = (
            "Configure the inter-switch interface as a trunk and "
            "allow the required VLANs."
        )

    # --------------------------------------------------------
    # NET-006 to NET-009 : Gateway
    # --------------------------------------------------------

    elif case_id == "NET-006":
        diagnosis = "Missing default gateway"
        explanation = (
            "The PC does not have a valid default gateway. "
            "Therefore, it cannot forward traffic to remote networks."
        )
        solution = (
            "Configure the PC's default gateway with the IP address "
            "of the router's LAN interface."
        )

    elif case_id == "NET-007":
        diagnosis = "Wrong default gateway"
        explanation = (
            "The configured default gateway does not match the "
            "router interface serving the PC's network."
        )
        solution = (
            "Replace the incorrect gateway with the correct "
            "router LAN interface address."
        )

    elif case_id == "NET-008":
        diagnosis = "Gateway interface is down"
        explanation = (
            "The router's LAN interface is administratively down, "
            "so the PC cannot communicate with its gateway."
        )
        solution = (
            "Enter the router interface configuration and use "
            "'no shutdown' to enable the interface."
        )

    elif case_id == "NET-009":
        diagnosis = "Gateway IP mismatch"
        explanation = (
            "The PC's configured gateway address does not match "
            "the router's LAN interface IP address."
        )
        solution = (
            "Configure the PC with the router's correct LAN "
            "interface IP as its default gateway."
        )

    # --------------------------------------------------------
    # NET-010 to NET-013 : DHCP
    # --------------------------------------------------------

    elif case_id == "NET-010":
        diagnosis = "DHCP pool missing"
        explanation = (
            "The router does not contain the required DHCP pool, "
            "so clients cannot obtain IP configuration."
        )
        solution = (
            "Create and configure the required DHCP pool on the router."
        )

    elif case_id == "NET-011":
        diagnosis = "Wrong DHCP network"
        explanation = (
            "The DHCP pool is configured for an incorrect network."
        )
        solution = (
            "Configure the DHCP pool with the correct network and "
            "subnet mask."
        )

    elif case_id == "NET-012":
        diagnosis = "Wrong DHCP default-router"
        explanation = (
            "The DHCP pool provides an incorrect default gateway "
            "to clients."
        )
        solution = (
            "Configure the DHCP pool with the correct "
            "default-router address."
        )

    elif case_id == "NET-013":
        diagnosis = "Wrong DHCP DNS server"
        explanation = (
            "The DHCP configuration provides an incorrect DNS "
            "server address to clients."
        )
        solution = (
            "Configure the correct DNS server address in the "
            "DHCP pool."
        )

    # --------------------------------------------------------
    # NET-014 to NET-016 : DNS
    # --------------------------------------------------------

    elif case_id == "NET-014":
        diagnosis = "Wrong DNS server"
        explanation = (
            "The client is configured to use an incorrect DNS server."
        )
        solution = (
            "Configure the client or DHCP pool with the correct "
            "DNS server address."
        )

    elif case_id == "NET-015":
        diagnosis = "DNS service disabled"
        explanation = (
            "The DNS service is disabled, so hostname resolution "
            "cannot work."
        )
        solution = (
            "Enable the DNS service on the configured DNS server."
        )

    elif case_id == "NET-016":
        diagnosis = "DNS record missing"
        explanation = (
            "The required DNS record does not exist, so the hostname "
            "cannot be resolved."
        )
        solution = (
            "Create the required DNS record and verify name resolution."
        )

    # --------------------------------------------------------
    # NET-017 to NET-020 : Routing
    # --------------------------------------------------------

    elif case_id == "NET-017":
        diagnosis = "Static route missing"
        explanation = (
            "The router does not contain the required route to "
            "the destination network."
        )
        solution = (
            "Add the required static route using the correct "
            "destination network and next hop."
        )

    elif case_id == "NET-018":
        diagnosis = "Wrong next hop"
        explanation = (
            "The static route uses an incorrect next-hop address."
        )
        solution = (
            "Modify the static route and configure the correct "
            "next-hop address."
        )

    elif case_id == "NET-019":
        diagnosis = "Router interface down"
        explanation = (
            "The router interface connecting the routed link is "
            "administratively down."
        )
        solution = (
            "Enter the affected interface and use 'no shutdown' "
            "to restore it."
        )

    elif case_id == "NET-020":
        diagnosis = "Default route missing"
        explanation = (
            "The router does not have a default route for "
            "unknown destination networks."
        )
        solution = (
            "Configure the appropriate default route toward "
            "the upstream router."
        )

    # --------------------------------------------------------
    # NET-021 to NET-023 : ACL
    # --------------------------------------------------------

    elif case_id == "NET-021":
        diagnosis = "ACL blocks ICMP"
        explanation = (
            "The ACL contains a rule that denies ICMP traffic, "
            "causing ping requests to fail."
        )
        solution = (
            "Modify the ACL so that required ICMP traffic is permitted."
        )

    elif case_id == "NET-022":
        diagnosis = "ACL blocks HTTP"
        explanation = (
            "The ACL blocks HTTP traffic between the client "
            "and web server."
        )
        solution = (
            "Modify the ACL to permit the required HTTP traffic."
        )

    elif case_id == "NET-023":
        diagnosis = "ACL applied in wrong direction or interface"
        explanation = (
            "The ACL is applied to an incorrect interface or direction, "
            "causing unintended traffic filtering."
        )
        solution = (
            "Apply the ACL to the correct interface and direction."
        )

    # --------------------------------------------------------
    # NET-024 to NET-026 : NAT
    # --------------------------------------------------------

    elif case_id == "NET-024":
        diagnosis = "NAT not configured"
        explanation = (
            "Network Address Translation is missing, so internal "
            "addresses cannot be translated for external communication."
        )
        solution = (
            "Configure the required NAT rules and identify the "
            "inside and outside interfaces."
        )

    elif case_id == "NET-025":
        diagnosis = "NAT inside/outside roles incorrect"
        explanation = (
            "The router interfaces have incorrect NAT inside/outside "
            "roles."
        )
        solution = (
            "Configure the correct interfaces as NAT inside and "
            "NAT outside."
        )

    elif case_id == "NET-026":
        diagnosis = "NAT ACL mismatch"
        explanation = (
            "The ACL used by NAT does not correctly identify the "
            "internal addresses that require translation."
        )
        solution = (
            "Correct the NAT ACL so that the intended internal "
            "network is permitted."
        )

    # --------------------------------------------------------
    # NET-027 to NET-030 : Wireless
    # --------------------------------------------------------

    elif case_id == "NET-027":
        diagnosis = "Wrong SSID"
        explanation = (
            "The configured wireless network name does not match "
            "the intended SSID."
        )
        solution = (
            "Configure the Access Point with the correct SSID "
            "and reconnect the wireless client."
        )

    elif case_id == "NET-028":
        diagnosis = "Wrong wireless password"
        explanation = (
            "The wireless password configured or entered by the "
            "client does not match."
        )
        solution = (
            "Configure and use the correct wireless security password."
        )

    elif case_id == "NET-029":
        diagnosis = "Wireless DHCP/network problem"
        explanation = (
            "The wireless client is unable to obtain a valid "
            "network configuration."
        )
        solution = (
            "Check wireless connectivity, DHCP configuration, "
            "IP addressing, and network settings."
        )

    elif case_id == "NET-030":
        diagnosis = "AP port VLAN mismatch"
        explanation = (
            "The switch port connected to the Access Point is "
            "assigned to an incorrect VLAN."
        )
        solution = (
            "Assign the AP switch port to the correct VLAN."
        )

    else:
        diagnosis = fault
        explanation = (
            "The case does not have a specific diagnosis rule yet."
        )
        solution = (
            "Inspect the evidence and network configuration manually."
        )

    return diagnosis, explanation, solution


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("==========================================")
    print("        NetSage AI Diagnosis Engine")
    print("==========================================")
    print()

    # --------------------------------------------------------
    # Check input file
    # --------------------------------------------------------

    if not os.path.exists(RULE_RESULTS_FILE):

        print(
            f"ERROR: Rule results file not found:\n"
            f"{RULE_RESULTS_FILE}"
        )

        print()
        print(
            "Run checker.py first."
        )

        return

    # --------------------------------------------------------
    # Load rule results
    # --------------------------------------------------------

    df = pd.read_csv(RULE_RESULTS_FILE)

    print(
        f"Loaded {len(df)} rule-checking results."
    )

    print()
    print("Generating diagnoses...")
    print()

    diagnosis_rows = []

    # --------------------------------------------------------
    # Generate diagnosis for every case
    # --------------------------------------------------------

    for _, row in df.iterrows():

        diagnosis, explanation, solution = generate_diagnosis(row)

        result = {
            "Case ID": row["Case ID"],
            "Category": row["Category"],
            "Expected Fault": row["Expected Fault"],
            "Rule": row["Rule"],
            "Status": row["Status"],
            "Finding": row["Finding"],
            "Diagnosis": diagnosis,
            "Explanation": explanation,
            "Recommended Solution": solution
        }

        diagnosis_rows.append(result)

        print(
            f'{row["Case ID"]:<10} | '
            f'{diagnosis}'
        )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    result_df = pd.DataFrame(diagnosis_rows)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("==========================================")
    print("        Diagnosis Completed")
    print("==========================================")
    print()

    print(
        f"Total Diagnoses : {len(result_df)}"
    )

    print()
    print("Results saved to:")
    print(OUTPUT_FILE)

    print()
    print("==========================================")


if __name__ == "__main__":
    main()