// This header file is used for test paramether definition
#ifndef __WIREGUARD__CONFIG__
#define __WIREGUARD__CONFIG__

#define WIREGUARD_INTERFACE_NAME "wg0"

#define WIREGUARD_IPV4NETWORK "10.0.2.0/26"

#define WIREGUARD_INTERFACE_ADDRESS "10.0.2.1"
#define WIREGUARD_INTERFACE_PORT 9876
#define WIREGUARD_SERVER_PUBLIC_KEY "GenerateAProperKeyToUseAsAWireguardEndpoint="
#define WIREGUARD_ENDPOINT "vpn.mydomain.com"

#define WIREGUARD_POOL_FIRST "10.0.2.2"
#define WIREGUARD_POOL_LAST "10.0.2.62"
#define WIREGUARD_DEFAULT_CLIENT_PORT 9876
#define WIREGUARD_NETWORK_MASK_SHORT 26

#define WIREGUARD_ENABLED False


#endif /* __WIREGUARD__CONFIG__ */
