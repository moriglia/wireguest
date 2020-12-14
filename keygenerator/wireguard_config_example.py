from ipaddress import IPv4Network

TUNNEL_NETWORK = IPv4Network('10.0.1.0/24')

# Assign first assignable address to Wireguard interface
SERVER_TUNNEL_ADDRESS = TUNNEL_NETWORK.network_address + 1

# Define a pool with all remaining assignable addresses in the network
CLIENT_POOL_FIRST = TUNNEL_NETWORK.network_address + 2
CLIENT_POOL_LAST = TUNNEL_NETWORK.broadcast_address - 1
