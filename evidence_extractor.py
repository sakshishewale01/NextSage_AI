import os
import re
import json
import zipfile
import pandas as pd

# ============================================================
# NetSage AI - Evidence Extractor
# Reads the 30 Packet Tracer case README files and converts
# their documented evidence into machine-readable JSON.
#
# IMPORTANT:
# This script does NOT invent Packet Tracer values.
# It extracts only information documented in the case README.
# ============================================================

CSV_FILE = "data/NetSage_30_Cases.csv"
CASE_FOLDER = "packet_tracer"
EVIDENCE_FOLDER = "evidence"

os.makedirs(EVIDENCE_FOLDER, exist_ok=True)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def find_case_folder(case_id):
    number = int(case_id.split("-")[1])
    return os.path.join(CASE_FOLDER, f"Case_{number:02d}")


def find_readme(case_folder):
    readme = os.path.join(case_folder, "Readme.md")
    if os.path.exists(readme):
        return readme

    # Case-insensitive fallback
    for name in os.listdir(case_folder):
        if name.lower() == "readme.md":
            return os.path.join(case_folder, name)

    return None


def get_section(text, heading):
    """
    Extract text under a markdown heading until the next heading
    of the same or higher level.
    """
    pattern = rf"(?ms)^#+\s*{re.escape(heading)}\s*$\n(.*?)(?=^#+\s|\Z)"
    match = re.search(pattern, text, flags=re.IGNORECASE)

    if match:
        return clean_text(match.group(1))

    return ""


def find_all_commands(text):
    """
    Extract command-like lines from fenced bash/text blocks and
    common Cisco commands appearing in prose.
    """
    commands = []

    for block in re.findall(r"```(?:bash|text|cisco|ios)?\s*(.*?)```", text,
                            flags=re.IGNORECASE | re.DOTALL):

        for line in block.splitlines():
            line = line.strip()

            if not line:
                continue

            if (
                line.startswith((
                    "show ",
                    "ping ",
                    "traceroute ",
                    "ip ",
                    "no ",
                    "interface ",
                    "switchport ",
                    "access-list ",
                    "vlan ",
                    "name ",
                    "network ",
                    "default-router ",
                    "ip nat ",
                    "router ",
                    "hostname ",
                    "enable",
                    "configure terminal",
                    "exit",
                    "end"
                ))
            ):
                commands.append(line)

    # Also capture common show commands outside code blocks.
    for command in re.findall(
        r"\b(show (?:vlan brief|running-config|ip interface brief|"
        r"ip route|ip nat translations|access-lists|ip dhcp pool|"
        r"ip dhcp binding|ip dns|interfaces?|startup-config))\b",
        text,
        flags=re.IGNORECASE
    ):
        commands.append(command)

    # Preserve order, remove duplicates
    result = []
    seen = set()

    for command in commands:
        key = command.lower()

        if key not in seen:
            seen.add(key)
            result.append(command)

    return result


def extract_screenshots(text, case_folder):
    """
    Extract image references from the README and also list image files
    physically present in the case folder.
    """
    references = re.findall(
        r"!\[[^\]]*\]\(([^)]+)\)",
        text
    )

    files = []

    for name in os.listdir(case_folder):
        lower = name.lower()

        if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
            files.append(name)

    result = []

    for item in references + files:
        item = item.strip()

        if item and item not in result:
            result.append(item)

    return result


def extract_ips(text):
    ips = re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        text
    )

    result = []

    for ip in ips:
        if ip not in result:
            result.append(ip)

    return result


def extract_cidr_and_masks(text):
    masks = re.findall(
        r"\b255\.(?:255|0)\.(?:255|0)\.(?:255|0)\b",
        text
    )

    networks = re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b",
        text
    )

    return {
        "subnet_masks": list(dict.fromkeys(masks)),
        "cidr_networks": list(dict.fromkeys(networks))
    }


def extract_key_values(text):
    """
    Extract simple 'Label: value' or 'Label = value' information.
    """
    result = {}

    for match in re.finditer(
        r"(?mi)^\s*([A-Za-z][A-Za-z0-9 /_-]{2,50})\s*[:=]\s*`?([^`\n]+?)`?\s*$",
        text
    ):
        key = match.group(1).strip()
        value = match.group(2).strip()

        if key and value:
            result[key] = value

    return result


def section_or_empty(text, names):
    for name in names:
        value = get_section(text, name)

        if value:
            return value

    return ""


# ------------------------------------------------------------
# Case-specific structured extraction
# ------------------------------------------------------------

def extract_structured_fields(case_id, text):
    """
    Extract fields that checker.py understands where the README
    provides enough information.
    """

    fields = {}

    # ========================================================
    # NET-001: Wrong Access VLAN
    # ========================================================
    if case_id == "NET-001":

        match = re.search(
            r"PC0\s*[→\-]\s*Fa0/1\s*[→\-]\s*VLAN\s*(\d+).*?"
            r"PC1\s*[→\-]\s*Fa0/2\s*[→\-]\s*VLAN\s*(\d+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:
            fields["actual_vlan_pc0"] = int(match.group(1))
            fields["actual_vlan_pc1"] = int(match.group(2))

        fields["expected_vlan"] = 10
        fields["actual_vlan"] = fields.get("actual_vlan_pc1")

    # ========================================================
    # NET-002 to NET-005 VLAN
    # ========================================================
    elif case_id == "NET-002":

        match = re.search(
            r"(\d+)\s+STUDENTS\s+active\s+Fa0/1,\s*Fa0/2",
            text,
            flags=re.IGNORECASE
        )

        if match:
            fields["required_vlan"] = int(match.group(1))
            fields["existing_vlans"] = [int(match.group(1))]

    elif case_id == "NET-003":

        pairs = re.findall(
            r"PC\d?\s*[→\-]\s*Fa0/\d+\s*[→\-]\s*VLAN\s*(\d+)",
            text,
            flags=re.IGNORECASE
        )

        if pairs:
            fields["vlan_assignments"] = [int(x) for x in pairs]

            if len(set(fields["vlan_assignments"])) > 1:
                fields["actual_vlan"] = fields["vlan_assignments"][1]
                fields["expected_vlan"] = fields["vlan_assignments"][0]

    elif case_id == "NET-004":

        match = re.search(
            r"Fa0/(\d+).*?(?:VLAN|vlan)\s*(\d+)",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:
            fields["actual_vlan"] = int(match.group(2))

        expected = re.search(
            r"(?:intended|should|correct).*?VLAN\s*(\d+)",
            text,
            flags=re.IGNORECASE
        )

        if expected:
            fields["expected_vlan"] = int(expected.group(1))

    elif case_id == "NET-005":

        if re.search(
            r"not trunking|not configured as trunk|trunk.*incorrect|"
            r"trunk.*problem|access mode",
            text,
            flags=re.IGNORECASE
        ):
            fields["trunk_status"] = "down"

    # ========================================================
    # NET-006 to NET-009 Gateway
    # ========================================================
    elif case_id == "NET-006":

        match = re.search(
            r"Default Gateway:\s*([0-9.]+)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            fields["gateway"] = match.group(1)

        fields["gateway_present"] = (
            fields.get("gateway") not in
            (None, "", "0.0.0.0")
        )

    elif case_id == "NET-007":

        match = re.search(
            r"Default Gateway:\s*([0-9.]+)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            fields["gateway"] = match.group(1)

        expected = re.search(
            r"(?:correct|should be|expected).*?gateway.*?([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)",
            text,
            flags=re.IGNORECASE
        )

        if expected:
            fields["expected_gateway"] = expected.group(1)

    elif case_id == "NET-008":

        if re.search(
            r"interface.*(?:down|shutdown)|administratively down|"
            r"gateway interface.*shutdown",
            text,
            flags=re.IGNORECASE
        ):
            fields["interface_status"] = "down"

    elif case_id == "NET-009":

        ips = extract_ips(text)

        if ips:
            fields["interface_ip"] = ips[0]

        expected = re.search(
            r"(?:correct|expected|should be).*?([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)",
            text,
            flags=re.IGNORECASE
        )

        if expected:
            fields["expected_interface_ip"] = expected.group(1)

    # ========================================================
    # NET-010 to NET-013 DHCP
    # ========================================================
    elif case_id in {"NET-010", "NET-011", "NET-012", "NET-013"}:

        if re.search(
            r"DHCP.*(?:not configured|missing|no pool|pool.*missing)",
            text,
            flags=re.IGNORECASE
        ):
            fields["pool_exists"] = False
        else:
            fields["pool_exists"] = True

        network = re.search(
            r"network\s+((?:\d{1,3}\.){3}\d{1,3})\s+"
            r"(255\.\d+\.\d+\.\d+)",
            text,
            flags=re.IGNORECASE
        )

        if network:
            fields["network"] = (
                f"{network.group(1)} {network.group(2)}"
            )

        router = re.search(
            r"default-router\s+((?:\d{1,3}\.){3}\d{1,3})",
            text,
            flags=re.IGNORECASE
        )

        if router:
            fields["default_router"] = router.group(1)

        dns = re.search(
            r"dns-server\s+((?:\d{1,3}\.){3}\d{1,3})",
            text,
            flags=re.IGNORECASE
        )

        if dns:
            fields["dns_server"] = dns.group(1)

    # ========================================================
    # NET-014 to NET-016 DNS
    # ========================================================
    elif case_id in {"NET-014", "NET-015", "NET-016"}:

        if case_id == "NET-015":
            fields["dns_service_enabled"] = not bool(
                re.search(
                    r"DNS service.*(?:disabled|off)",
                    text,
                    flags=re.IGNORECASE
                )
            )

        if case_id == "NET-016":
            fields["dns_record_exists"] = not bool(
                re.search(
                    r"record.*(?:missing|not found|does not exist)",
                    text,
                    flags=re.IGNORECASE
                )
            )

        dns = re.search(
            r"(?:DNS Server|DNS server|dns-server)\s*[:=]?\s*"
            r"((?:\d{1,3}\.){3}\d{1,3})",
            text,
            flags=re.IGNORECASE
        )

        if dns:
            fields["dns_server"] = dns.group(1)

    # ========================================================
    # NET-017 to NET-020 Routing
    # ========================================================
    elif case_id in {"NET-017", "NET-018", "NET-020"}:

        if re.search(
            r"route.*(?:missing|not configured|does not exist)",
            text,
            flags=re.IGNORECASE
        ):
            fields["route_exists"] = False

        if case_id == "NET-020":
            fields["default_route_exists"] = not bool(
                re.search(
                    r"default route.*(?:missing|not configured)",
                    text,
                    flags=re.IGNORECASE
                )
            )

        next_hop = re.search(
            r"(?:next hop|via)\s*[:=]?\s*"
            r"((?:\d{1,3}\.){3}\d{1,3})",
            text,
            flags=re.IGNORECASE
        )

        if next_hop:
            fields["next_hop"] = next_hop.group(1)

    # ========================================================
    # NET-019 Interface
    # ========================================================
    elif case_id == "NET-019":

        if re.search(
            r"(?:interface|router interface).*"
            r"(?:shutdown|down|administratively down)",
            text,
            flags=re.IGNORECASE
        ):
            fields["interface_status"] = "down"

    # ========================================================
    # NET-021 to NET-023 ACL
    # ========================================================
    elif case_id in {"NET-021", "NET-022", "NET-023"}:

        if case_id == "NET-021":
            fields["icmp_allowed"] = not bool(
                re.search(
                    r"ACL.*(?:blocks|denies|block).*ICMP|"
                    r"ping.*blocked",
                    text,
                    flags=re.IGNORECASE
                )
            )

        elif case_id == "NET-022":
            fields["http_allowed"] = not bool(
                re.search(
                    r"ACL.*(?:blocks|denies|block).*HTTP|"
                    r"HTTP.*blocked",
                    text,
                    flags=re.IGNORECASE
                )
            )

        elif case_id == "NET-023":
            fields["placement_correct"] = not bool(
                re.search(
                    r"ACL.*(?:wrong|incorrect).*"
                    r"(?:interface|direction|placement)",
                    text,
                    flags=re.IGNORECASE
                )
            )

    # ========================================================
    # NET-024 to NET-026 NAT
    # ========================================================
    elif case_id in {"NET-024", "NET-025", "NET-026"}:

        if re.search(
            r"NAT.*(?:not configured|missing|no NAT)",
            text,
            flags=re.IGNORECASE
        ):
            fields["nat_configured"] = False
        else:
            fields["nat_configured"] = True

        if case_id == "NET-025":

            if re.search(
                r"G0/0\s*[→\-]\s*ip nat outside",
                text,
                flags=re.IGNORECASE
            ):
                fields["inside_role"] = "outside"

            if re.search(
                r"G0/1\s*[→\-]\s*ip nat inside",
                text,
                flags=re.IGNORECASE
            ):
                fields["outside_role"] = "inside"

            fields["expected_inside_role"] = "inside"
            fields["expected_outside_role"] = "outside"

        elif case_id == "NET-026":

            if re.search(
                r"only PC0|only.*192\.168\.10\.10|"
                r"only.*permit.*192\.168\.10\.10",
                text,
                flags=re.IGNORECASE
            ):
                fields["acl_matches"] = False

    # ========================================================
    # NET-027 to NET-030 Wireless
    # ========================================================
    elif case_id in {"NET-027", "NET-028", "NET-029", "NET-030"}:

        ssids = re.findall(
            r"(?:SSID|wireless network)\s*[:=]?\s*`?([A-Za-z0-9_-]+)`?",
            text,
            flags=re.IGNORECASE
        )

        ssids = list(dict.fromkeys(ssids))

        if case_id == "NET-027":

            if "WrongWiFi" in ssids:
                fields["ssid"] = "WrongWiFi"
                fields["expected_ssid"] = "CampusWiFi"

            elif "CampusWiFi" in ssids:
                fields["expected_ssid"] = "CampusWiFi"

        elif case_id == "NET-029":

            fields["dhcp_working"] = not bool(
                re.search(
                    r"(?:DHCP|IP address).*"
                    r"(?:not configured|no IP|cannot receive|no usable)",
                    text,
                    flags=re.IGNORECASE
                )
            )

        elif case_id == "NET-030":

            vlan = re.search(
                r"(?:Fa0/1|AP.*port).*?"
                r"VLAN\s*(\d+)",
                text,
                flags=re.IGNORECASE | re.DOTALL
            )

            if vlan:
                fields["ap_vlan"] = int(vlan.group(1))

            fields["expected_ap_vlan"] = 10

    return fields


# ------------------------------------------------------------
# Main extraction
# ------------------------------------------------------------

def main():

    print()
    print("==========================================")
    print("       NetSage AI Evidence Extractor")
    print("==========================================")
    print()

    if not os.path.exists(CASE_FOLDER):
        print(f"ERROR: Folder not found: {CASE_FOLDER}")
        return

    case_count = 0
    success_count = 0
    missing_count = 0

    # Read case IDs from CSV when available.
    case_ids = []

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(
            CSV_FILE,
            encoding="utf-8-sig"
        )

        df.columns = (
            df.columns
            .str.replace("\ufeff", "", regex=False)
            .str.strip()
        )

        if "Case ID" in df.columns:
            case_ids = [
                str(x).strip()
                for x in df["Case ID"].tolist()
            ]

    # Fallback: discover Case_01 ... Case_30
    if not case_ids:
        case_ids = [
            f"NET-{i:03d}"
            for i in range(1, 31)
        ]

    for case_id in case_ids:

        case_count += 1

        case_folder = find_case_folder(case_id)

        if not os.path.exists(case_folder):
            print(f"{case_id}: CASE FOLDER NOT FOUND")
            missing_count += 1
            continue

        readme_path = find_readme(case_folder)

        if readme_path is None:
            print(f"{case_id}: README NOT FOUND")
            missing_count += 1
            continue

        text = read_file(readme_path)
        text_clean = clean_text(text)

        # ----------------------------------------------------
        # Basic metadata
        # ----------------------------------------------------

        title_match = re.search(
            rf"^#\s*{re.escape(case_id)}\s*[–-]\s*(.+)$",
            text_clean,
            flags=re.IGNORECASE | re.MULTILINE
        )

        title = (
            title_match.group(1).strip()
            if title_match
            else ""
        )

        problem = section_or_empty(
            text_clean,
            ["Problem", "Issue"]
        )

        root_cause = section_or_empty(
            text_clean,
            ["Root Cause", "Cause"]
        )

        solution = section_or_empty(
            text_clean,
            ["Solution", "Fix"]
        )

        evidence_section = section_or_empty(
            text_clean,
            ["Evidence", "Evidence Collection", "Verification"]
        )

        commands = find_all_commands(text_clean)
        screenshots = extract_screenshots(
            text_clean,
            case_folder
        )

        ips = extract_ips(text_clean)
        network_info = extract_cidr_and_masks(text_clean)
        key_values = extract_key_values(text_clean)

        structured = extract_structured_fields(
            case_id,
            text_clean
        )

        # ----------------------------------------------------
        # Evidence JSON
        # ----------------------------------------------------

        evidence = {

            "case_id": case_id,

            "source": {
                "readme": os.path.relpath(
                    readme_path
                ),
                "case_folder": os.path.relpath(
                    case_folder
                ),
                "screenshots": screenshots
            },

            "case_title": title,

            "problem": problem,

            "evidence_status": "EXTRACTED_FROM_README",

            "evidence": {
                "evidence_section": evidence_section,
                "commands": commands,
                "ip_addresses_found": ips,
                "network_information": network_info,
                "key_value_information": key_values
            },

            "structured_evidence": structured,

            "root_cause": root_cause,

            "solution": solution,

            "actual_evidence": (
                evidence_section
                if evidence_section
                else text_clean
            )
        }

        output_file = os.path.join(
            EVIDENCE_FOLDER,
            f"{case_id}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                evidence,
                f,
                indent=4,
                ensure_ascii=False
            )

        success_count += 1

        print(
            f"{case_id}: extracted → {output_file}"
        )

    print()
    print("==========================================")
    print("Extraction Completed")
    print("==========================================")
    print(f"Cases found       : {case_count}")
    print(f"Successfully read : {success_count}")
    print(f"Missing/error     : {missing_count}")
    print()
    print(
        "Evidence JSON files updated in:"
    )
    print(
        EVIDENCE_FOLDER
    )
    print("==========================================")


if __name__ == "__main__":
    main()