from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from ipaddress import IPv4Address, IPv4Network
from . import wireguard_config as wgc


# Classes and function to test
from .models import Peer
from .peer_interface_registration import get_next_ip_from_pool, \
    registrate_interface


class Test_050_Peer(TestCase):

    def test_00_maxip_with_no_peer_interface(self):
        self.assertIsNone(Peer.maxip())

    def test_05_maxip(self):
        users = []
        peers = []
        base_addr = IPv4Address('192.168.0.1')
        addr = []
        for i in range(20):
            users.append(mommy.make(User))
            addr.append(base_addr + i)
            assert (base_addr + i) == addr[-1]
            peers.append(
                Peer(
                    name=f"{users[-1].username}_{i}",
                    user=users[-1],
                    address=addr[-1],
                    public_key=""  # Rimember to implement test
                )
            )
            peers[-1].save()

            maxip = Peer.maxip()
            self.assertIsNotNone(maxip)
            self.assertIsInstance(maxip, IPv4Address)
            self.assertEqual(maxip, addr[-1])

        self.assertEqual(Peer.maxip(), max(addr))


class Test_060_PeerInterfaceRegistration(TestCase):

    def verify_addr(self, addr):
        if addr < wgc.CLIENT_POOL_FIRST:
            self.assertIsNone(get_next_ip_from_pool(addr))

        elif addr > wgc.CLIENT_POOL_LAST:
            self.assertIsNone(get_next_ip_from_pool(addr))

        elif addr == wgc.CLIENT_POOL_LAST:
            self.assertEqual(
                get_next_ip_from_pool(addr),
                wgc.CLIENT_POOL_FIRST
            )
        else:
            self.assertEqual(get_next_ip_from_pool(addr), addr + 1)

    def test_10_get_next_ip_from_pool(self):
        self.assertEqual(get_next_ip_from_pool(None), wgc.CLIENT_POOL_FIRST)

        inputs_None_expected = [
            "string",
            12,
            ['c', 12],
            wgc.CLIENT_POOL_FIRST - 1,
            wgc.CLIENT_POOL_LAST + 1
        ]

        for i in inputs_None_expected:
            self.assertIsNone(get_next_ip_from_pool(i))

        # Check a subset of the private networks
        # Make sure at list one of the networks
        # includes the pool
        for addr in IPv4Network('10.0.2.0/24'):
            self.verify_addr(addr)

        for addr in IPv4Network('192.168.0.0/24'):
            self.verify_addr(addr)

        for addr in IPv4Network('172.16.0.0/24'):
            self.verify_addr(addr)

    def test_20_registrate_interface(self):
        u = mommy.make(User)

        ip = registrate_interface(u, "First Interface")

        p = Peer.objects.first()

        self.assertIsNotNone(p)
        self.assertIsInstance(p, Peer)

        self.assertEqual(p.address, wgc.CLIENT_POOL_FIRST)
        self.assertEqual(ip, wgc.CLIENT_POOL_FIRST)
        self.assertEqual(p.name, "First Interface")

        # Assume we do not reach the end of the pool
        for count in range(10):
            last_interface_address = Peer.maxip() + 1
            self.assertEqual(
                last_interface_address,
                registrate_interface(u, "Generic Name")
            )
            self.assertEqual(
                Peer.objects.last().address,
                last_interface_address
            )

        # Add a peer with the last address of the pool (leaving some available)
        # IP addresses in the middle of the pool
        p = Peer(user=u, name="Last", address=wgc.CLIENT_POOL_LAST)
        p.save()

        # Since there is a peer interface with ip equal to the last of the pool
        # the function should loop and restart searching for an available ip
        # starting from the first address of the pool
        self.assertEqual(
            registrate_interface(u, "Another one"),
            last_interface_address + 1
        )

        # Fill all remaining interfaces in the pool
        while registrate_interface(u, "Filling") != wgc.CLIENT_POOL_LAST - 1:
            pass

        # The next interface will not be inserted because pool is completely
        # allocated
        self.assertIsNone(registrate_interface(u, "NOT_IN_DATABASE"))
        query = Peer.objects.filter(name="NOT_IN_DATABASE")
        self.assertEqual(query.count(), 0)
