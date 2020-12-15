from django.test import TestCase
from .models import Peer
from django.contrib.auth.models import User
from model_mommy import mommy
from ipaddress import IPv4Address


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
