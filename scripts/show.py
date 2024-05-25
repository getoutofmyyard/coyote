# Show command set

show_params = {
    "show arp": ["ifIndex", "InterfaceAlias", "LinkLayerAddress", "IPAddress", "State"],
    "show nic": ["ifIndex", "InterfaceAlias", "MacAddress", "Status", "AdminStatus", "LinkSpeed", "DriverProvider", "DriverVersion"],
    "show ip address":["ifIndex","InterfaceAlias","IPAddress","PrefixLength","PrefixOrigin"],
    "show vpn":["Name","ServerAddress","TunnelType","IPSecCustomPolicy","AuthenticationMethod","ConnectionStatus","SplitTunneling","RememberCredential"]
}

show_commands = {
    "show arp":f"Get-NetNeighbor -State Reachable,Stale | Select-Object -Property {", ".join(show_params.get("show arp"))} | ConvertTo-Json",
    "show bgp aggregate":"Get-BgpRouteAggregate",
    "show bgp advertise":"Get-BgpCustomRoute",
    "show bgp id":"Get-BgpRouter | Select-Object BgpIdentifier, LocalASN, TransitRouting, RouteReflector | Format-List",
    "show bgp peer":"Get-BgpPeer -Verbose | Format-List",
    "show bgp status":"Get-BgpStatistics",
    "show dns cache":"Get-DnsClientCache | Sort-Object -Property Entry | Format-Table -AutoSize",
    "show dns server":"Get-DnsClientServerAddress | Sort-Object -Property AddressFamily | Format-Table -Autosize",
    "show drives":"Get-Volume",
    "show fwall profile":"Get-NetFirewallProfile",
    "show gpo":"gpresult /R",
    "show nic":f"Get-NetAdapter | Select-Object -Property {", ".join(show_params.get("show nic"))} | ConvertTo-Json",
    "show ip address":f"Get-NetIPAddress -AddressFamily IPv4 | Select-Object -Property {", ".join(show_params.get("show ip address"))} | ConvertTo-Json",
    "show ip public":"(Invoke-WebRequest https://itomation.ca/mypublicip).content",
    "show ip route":"Get-NetRoute -AddressFamily ipv4 | Sort-Object -Property DestinationPrefix | Format-Table -Autosize",
    "show ipv6 address":"Get-NetIPAddress -AddressFamily IPv6 | Select-Object -Property ifIndex,InterfaceAlias,IPAddress,PrefixLength,PrefixOrigin | Sort-Object -Property IPAddress | Format-Table -AutoSize",
    "show ipv6 public":"(Invoke-WebRequest ip6only.me/api/).content",
    "show ipv6 route":"Get-NetRoute -AddressFamily ipv6 | Sort-Object -Property DestinationPrefix | Format-Table -Autosize",
    "show log wev":"eventvwr.msc",
    "show powershell version":"$PSVersionTable | Format-Table -HideTableHeaders",
    "show proc top":"Get-Process | Sort-Object -Property WS | Select-Object -Last 10 | sort-object -Property CPU -Descending",
    "show proc":"Get-Process | Sort-Object -Property CPU -Descending",
    "show programs":r"Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize",
    "show svc":"Get-Service | Sort-Object -Property Status -Descending | Format-Table -AutoSize",
    "show tcp":"netstat -n",
    "show vpn":f"Get-VpnConnection | Select-Object -Property {", ".join(show_params.get("show vpn"))} | ConvertTo-Json",
    "notfound":"notfound",
}
