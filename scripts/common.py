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

def decode_win_json(data):
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
    terminal_width = shutil.get_terminal_size().columns
    pandas.set_option("display.max_columns", None)  # Display all columns
    pandas.set_option("display.width", terminal_width)  # Auto-detect screen width and avoid wrapping
    pandas.set_option("display.colheader_justify", "center")  # Center column headers
    pandas.set_option("display.expand_frame_repr", False)  # Disable wrapping

    filtered_df = data_frame[params]

    table = tabulate(filtered_df, headers="keys", tablefmt="pretty",stralign="right",showindex=False)

    print(table)
