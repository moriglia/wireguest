from django.db import models
from ipaddress import IPv4Address, AddressValueError


class IPv4AddressField(models.CharField):

    description = "IPv4 address"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

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
        return str(value)
