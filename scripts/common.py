import subprocess, json, pandas, ipaddress, shutil
from tabulate import tabulate

def newline():
    print("")

def read_file(filepath):
    # Reads a file. Used most often for help files.
    try:
        with open(filepath,"r") as file:
            print(file.read())
            newline()
    except:
        newline()
        print("error~! Help file " + filepath + " is missing.")
        newline()

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(["powershell.exe", command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode("iso-8859-1")
    return decoded_output.strip()

def convert_bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)

def paginate_output(output, page_size=50):
    lines = output.splitlines()
    total_lines = len(lines)
    for start in range(0, total_lines, page_size):
        end = start + page_size
        page = lines[start:end]
        for line in page:
            print(line)
        if end < total_lines:
            input("Press Enter to continue...")

def decode_win_json(data):

    dns_section_map = {
        0: "Reserved",
        1: "Answer",
        2: "Authority",
        3: "Additional"
    }

    dns_status_map = {
        0: "Success",
        1: "FormErr",
        2: "ServFail",
        3: "NXDomain",
        4: "NotImp",
        5: "Refused",
        6: "YXDomain",
        7: "YXRRSet",
        8: "NXRRSet",
        9: "NotAuth",
        10: "NotZone"
    }


    dns_type_map = {
        1: "A (Host Address)",
        2: "NS (Authoritative Name Server)",
        5: "CNAME (Canonical Name)",
        6: "SOA (Start of a Zone of Authority)",
        12: "PTR (Domain Name Pointer)",
        15: "MX (Mail Exchange)",
        16: "TXT (Text Strings)",
        28: "AAAA (IPv6 Address)",
        33: "SRV (Service Locator)",
        252: "AXFR (Transfer of an entire zone)",
        255: "ANY (Wildcard match)"
    }

    state_map = {
        0: "Unreachable",
        1: "Incomplete",
        2: "Probe",
        3: "Delay",
        4: "Stale",
        5: "Reachable",
        6: "Permanent"
    }
    
    store_map = {
        0: "ActiveStore",
        1: "PersistentStore",
        2: "All"
    }
    
    address_family_map = {
        2: "IPv4",
        23: "IPv6"
    }
    
    operational_status_map = {
        1: "Up",
        2: "Down",
        3: "Testing",
        4: "Unknown",
        5: "Dormant",
        6: "NotPresent",
        7: "LowerLayerDown"
    }

    admin_status_map = {
        1: "Up",
        2: "Down",
        3: "Testing"
    }

    media_connection_state_map = {
        1: "Connected",
        2: "Disconnected"
    }

    enabled_default_map = {
        2: "Enabled",
        3: "Disabled"
    }

    enabled_state_map = {
        2: "Enabled",
        3: "Disabled",
        5: "Enabled",
        12: "Disabled"
    }

    requested_state_map = {
        1: "Enabled",
        2: "Disabled",
        3: "Shutting Down",
        4: "No Change",
        5: "Reset",
        6: "Power Off",
        7: "Offline",
        8: "Test",
        9: "Defer",
        10: "Quiesce",
        11: "Reboot",
        12: "Resetting"
    }

    prefix_origin_map = {
        1: "Manual",
        2: "WellKnown",
        3: "DHCP",
        4: "RouterAdvertisement",
        5: "Other"
    }

    protocol_map = {
        1: "Other",
        2: "Local",
        3: "NetMgmt",
        4: "ICMP",
        5: "EGP",
        6: "GGP",
        7: "Hello",
        8: "RIP",
        9: "Is-Is",
        10: "ES-IS",
        11: "CISCO",
        12: "BBN",
        13: "OSPF",
        14: "BGP",
        15: "ND",
        16: "EIGRP"
    }

    cidr_mask_map = {
        0:"0.0.0.0",
        1:"128.0.0.0",
        2:"192.0.0.0",
        3:"224.0.0.0",
        4:"240.0.0.0",
        5:"248.0.0.0",
        6:"252.0.0.0",
        7:"254.0.0.0",
        8:"255.0.0.0",
        9:"255.128.0.0",
        10:"255.192.0.0",
        11:"255.224.0.0",
        12:"255.240.0.0",
        13:"255.248.0.0",
        14:"255.252.0.0",
        15:"255.254.0.0",
        16:"255.255.0.0",
        17:"255.255.128.0",
        18:"255.255.192.0",
        19:"255.255.224.0",
        20:"255.255.240.0",
        21:"255.255.248.0",
        22:"255.255.252.0",
        23:"255.255.254.0",
        24:"255.255.255.0",
        25:"255.255.255.128",
        26:"255.255.255.192",
        27:"255.255.255.224",
        28:"255.255.255.240",
        29:"255.255.255.248",
        30:"255.255.255.252",
        31:"255.255.255.254",
        32:"255.255.255.255",
        33: "/33",
        34: "/34",
        35: "/35",
        36: "/36",
        37: "/37",
        38: "/38",
        39: "/39",
        40: "/40",
        41: "/41",
        42: "/42",
        43: "/43",
        44: "/44",
        45: "/45",
        46: "/46",
        47: "/47",
        48: "/48",
        49: "/49",
        50: "/50",
        51: "/51",
        52: "/52",
        53: "/53",
        54: "/54",
        55: "/55",
        56: "/56",
        57: "/57",
        58: "/58",
        59: "/59",
        60: "/60",
        61: "/61",
        62: "/62",
        63: "/63",
        64: "/64",
        65: "/65",
        66: "/66",
        67: "/67",
        68: "/68",
        69: "/69",
        70: "/70",
        71: "/71",
        72: "/72",
        73: "/73",
        74: "/74",
        75: "/75",
        76: "/76",
        77: "/77",
        78: "/78",
        79: "/79",
        80: "/80",
        81: "/81",
        82: "/82",
        83: "/83",
        84: "/84",
        85: "/85",
        86: "/86",
        87: "/87",
        88: "/88",
        89: "/89",
        90: "/90",
        91: "/91",
        92: "/92",
        93: "/93",
        94: "/94",
        95: "/95",
        96: "/96",
        97: "/97",
        98: "/98",
        99: "/99",
        100: "/100",
        101: "/101",
        102: "/102",
        103: "/103",
        104: "/104",
        105: "/105",
        106: "/106",
        107: "/107",
        108: "/108",
        109: "/109",
        110: "/110",
        111: "/111",
        112: "/112",
        113: "/113",
        114: "/114",
        115: "/115",
        116: "/116",
        117: "/117",
        118: "/118",
        119: "/119",
        120: "/120",
        121: "/121",
        122: "/122",
        123: "/123",
        124: "/124",
        125: "/125",
        126: "/126",
        127: "/127",
        128: "/128",
    }

    transitioning_to_state_map = requested_state_map  # Reuse the same map as requested_state_map
    if_oper_status_map = operational_status_map

    for item in data:
        if "State" in item:
            item["State"] = state_map.get(item["State"], item["State"])
        if "Store" in item:
            item["Store"] = store_map.get(item["Store"], item["Store"])
        if "AddressFamily" in item:
            item["AddressFamily"] = address_family_map.get(item["AddressFamily"], item["AddressFamily"])
        if "InterfaceOperationalStatus" in item:
            item["InterfaceOperationalStatus"] = operational_status_map.get(item["InterfaceOperationalStatus"], item["InterfaceOperationalStatus"])
        if "AdminStatus" in item:
            item["AdminStatus"] = admin_status_map.get(item["AdminStatus"], item["AdminStatus"])
        if "MediaConnectionState" in item:
            item["MediaConnectionState"] = media_connection_state_map.get(item["MediaConnectionState"], item["MediaConnectionState"])
        if "EnabledDefault" in item:
            item["EnabledDefault"] = enabled_default_map.get(item["EnabledDefault"], item["EnabledDefault"])
        if "EnabledState" in item:
            item["EnabledState"] = enabled_state_map.get(item["EnabledState"], item["EnabledState"])
        if "RequestedState" in item:
            item["RequestedState"] = requested_state_map.get(item["RequestedState"], item["RequestedState"])
        if "TransitioningToState" in item:
            item["TransitioningToState"] = transitioning_to_state_map.get(item["TransitioningToState"], item["TransitioningToState"])
        if "ifOperStatus" in item:
            item["ifOperStatus"] = if_oper_status_map.get(item["ifOperStatus"], item["ifOperStatus"])
        if "PrefixLength" in item:
            item["PrefixLength"] = cidr_mask_map.get(item["PrefixLength"], item["PrefixLength"])
        if "PrefixOrigin" in item:
            item["PrefixOrigin"] = prefix_origin_map.get(item["PrefixOrigin"], item["PrefixOrigin"])
        if "Size" in item:
            item["Size"] = str(convert_bytes_to_gb(item['Size'])) + " GB"
        if "SizeRemaining" in item:
            item["SizeRemaining"] = str(convert_bytes_to_gb(item['SizeRemaining'])) + " GB"
        if "Section" in item:
            item["Section"] = dns_section_map.get(item["Section"], item["Section"])
        if "Type" in item and not "TunnelType" in item:
            item["Type"] = dns_type_map.get(item["Type"], item["Type"])
        if "Protocol" in item:
            item["Protocol"] = protocol_map.get(item["Protocol"], item["Protocol"])

    return data

def parse_json(in_file, params):
    
    init = json.loads(in_file)
    data = decode_win_json(init)

    # Create data frame using powershell json output
    data_frame = pandas.DataFrame(data)

    # Sort IP addresses in the table when needed

    if "IPAddress" in data_frame.columns:
        data_frame["IPAddressNum"] = data_frame["IPAddress"].apply(lambda ip: int(ipaddress.IPv4Address(ip)))
        data_frame = data_frame.sort_values(by="IPAddressNum")
        data_frame = data_frame.drop(columns=["IPAddressNum"])
        data_frame = data_frame.reset_index(drop=True)
    elif "ifAlias" in data_frame.columns:
        data_frame = data_frame.sort_values(by="ifAlias")
        data_frame = data_frame.reset_index(drop=True)
    else:
        pass

    # Set pandas display options
    try:
        terminal_width = shutil.get_terminal_size().columns
        pandas.set_option("display.max_columns", None)  # Display all columns
        pandas.set_option("display.width", terminal_width)  # Auto-detect screen width and avoid wrapping
        pandas.set_option("display.colheader_justify", "center")  # Center column headers
        pandas.set_option("display.expand_frame_repr", False)  # Disable wrapping

        filtered_df = data_frame[params]

        table = tabulate(filtered_df, headers="keys", tablefmt="pretty",stralign="right",showindex=False)

        print("\n".join([line[:terminal_width] for line in table.split("\n")]))

    except:
        print(in_file)
