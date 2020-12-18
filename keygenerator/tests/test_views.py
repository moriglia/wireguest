from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from model_mommy import mommy

from ..models import Peer
from ..peer_interface_registration import get_next_ip_from_pool


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
