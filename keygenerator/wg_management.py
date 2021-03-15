# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from .wireguard_config import WG_INTERFACE_NAME, WG_ENABLED
from os import system


def wg_set_peer(peer):
    if not WG_ENABLED:
        return

    system(
        f"wg set {WG_INTERFACE_NAME} "
        f"peer {peer.public_key} "
        f"allowed-ips {peer.address}/32"
    )


def wg_delete_peer(peer_public_key):
    if not WG_ENABLED:
        return

    system(
        f"wg set {WG_INTERFACE_NAME}"
        f"peer {peer_public_key} remove"
    )
