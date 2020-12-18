# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from django.db import models
from ipaddress import IPv4Address, AddressValueError


class IPv4AddressField(models.PositiveBigIntegerField):

    description = "IPv4 address"

    @staticmethod
    def parse_address_or_None(value):
        try:
            value = IPv4Address(value)
        except AddressValueError:
            value = None

        return value

    def from_db_value(self, value, expression, connection):
        return IPv4AddressField.parse_address_or_None(value)

    def to_python(self, value):
        return IPv4AddressField.parse_address_or_None(value)

    def get_prep_value(self, value):
        return int(value)
