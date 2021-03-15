# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from ipaddress import IPv4Address
from .wireguard_config import CLIENT_POOL_FIRST, CLIENT_POOL_LAST
from .models import Peer
from django.db.utils import DatabaseError
from django.db import transaction


def get_next_ip_from_pool(ip):
    if ip is None:
        return CLIENT_POOL_FIRST

    # We expect ip to be in the pool
    if not isinstance(ip, IPv4Address)\
        or ip < CLIENT_POOL_FIRST\
            or ip > CLIENT_POOL_LAST:
        return None

    # Get next IP
    ip += 1

    # Wrap the pool
    if ip > CLIENT_POOL_LAST:
        ip = CLIENT_POOL_FIRST

    return ip


def registrate_interface(user, interface_name, interface_public_key):
    preceding_ip = Peer.maxip()

    if preceding_ip is None:
        # No peer interface has been registered yet
        # Concurrency might still occur
        preceding_ip = CLIENT_POOL_LAST

    ip = get_next_ip_from_pool(preceding_ip)
    while ip != preceding_ip:
        # Look for an unused IP in the pool as long as we don't do
        # a complete visit of the pool

        # Try to save the new peer interface
        p = Peer(
            name=interface_name,
            user=user,
            address=ip,
            public_key=interface_public_key
        )
        try:
            with transaction.atomic():
                p.save()

            # Exit if successfully saved a UNIQUE ip address
            return p
        except DatabaseError:
            # Try the next ip in the pool if there already was the selected ip
            # in the Peer interface table
            ip = get_next_ip_from_pool(ip)

    # There was no available IP in the pool
    # no interface has been saved
    return None
