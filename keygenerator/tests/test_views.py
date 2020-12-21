from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from .utils import randomKey

from ..models import Peer
from ..peer_interface_registration import (
    get_next_ip_from_pool, registrate_interface,
)


class Test_070_HomeView(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = mommy.make(User)
        self.u.save()

    def test_05_home_no_login(self):
        # Redirect to login page
        r = self.c.get(reverse('keygen-home'))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(hasattr(r, 'url'))
        self.assertIn('login', r.url)

    def inspect_home_view(self, numkeys):
        self.c.force_login(self.u)

        # get home
        r = self.c.get(reverse('keygen-home'))
        self.assertEqual(r.status_code, 200)

        # check the number of keys displayed
        self.assertEqual(len(r.context['peers']), numkeys)

    def test_20_home_view(self):
        self.inspect_home_view(0)

        # Make some keys
        numkeys = 5
        keys = []
        for k in range(numkeys):
            addr = get_next_ip_from_pool(Peer.maxip())
            keys.append(mommy.make(Peer, user=self.u, address=addr))
            keys[-1].save()

        self.inspect_home_view(numkeys)


class Test_080_CreateView(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = mommy.make(User)
        self.keys = []
        self.num_interfaces = 20

    def submit_key(self, interface_name, interface_key=None):
        if interface_key is None:
            interface_key = randomKey()
        return self.c.post(
            reverse('keygen-create'),
            {
                "interface_name": interface_name,
                "interface_public_key": interface_key
            } if interface_name else None
        )

    def test_10_get_create_view(self):
        # Try a get with no login
        r = self.c.get(reverse('keygen-create'))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(hasattr(r, 'url'))
        self.assertIn('login', r.url)

        # Try a post with no login
        r = self.submit_key("wg-not-appearing-interface")
        self.assertEqual(r.status_code, 302)

        # Login
        self.c.force_login(self.u)

        # Correctly get to the interface registration page
        r = self.c.get(reverse('keygen-create'))
        self.assertEqual(r.status_code, 200)

    def test_20_submit_peer_interface(self):
        self.c.force_login(self.u)

        interface_names = []
        for k in range(self.num_interfaces):
            interface_names.append(f"wg{k}")
            r = self.submit_key(interface_names[-1])
            self.assertEqual(r.status_code, 200)

            # The viw does not immediately redirect to the home page any more
            # self.assertEqual(r.status_code, 302)
            # self.assertTrue(hasattr(r, 'url'))
            # self.assertEqual(reverse('keygen-home'), r.url)

        # Check registered interfaces in home view
        r = self.c.get(reverse('keygen-home'))

        self.assertEqual(len(r.context['peers']), self.num_interfaces)
        for peer in r.context['peers']:
            self.assertEqual(peer.user, self.u)
            self.assertIn(peer.name, interface_names)
            interface_names.remove(peer.name)

        # No interface remains
        self.assertEqual(len(interface_names), 0)

    def test_30_submit_bogus_interface(self):
        self.c.force_login(self.u)

        # invalid names
        invalid_interface_names = [None, False]
        for invalid_name in invalid_interface_names:
            r = self.submit_key(invalid_name)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['messages']), 1)
            for message in r.context['messages']:
                self.assertEqual(str(message), "Invalid interface data")

        # invalid_public_keys
        invalid_public_keys = [3, "ll", [0, 2, 'a'], (0, 1, 2, 3), True]
        for invalid_key in invalid_public_keys:
            r = self.submit_key("Valid Name but...", invalid_key)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['messages']), 1)
            for message in r.context['messages']:
                self.assertEqual(str(message), "Invalid interface data")

    def test_40_full_pool(self):
        # Fill pool with interfaces
        k = 0
        while registrate_interface(
            self.u,
            f"wg{k}-self.u.username",
            randomKey()
        ):
            k += 1
            pass

        self.c.force_login(self.u)

        r = self.submit_key("Any-Name")
        self.assertEqual(r.status_code, 200)

        # self.assertEqual(len(r.context['messages']), 1)
        # for message in r.context['messages']:
        #     self.assertEqual(
        #         str(message),
        #         "Unable to create interface Any-Name for "
        #         f"{self.u.username}"
        #     )
