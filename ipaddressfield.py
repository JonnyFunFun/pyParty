from django.db import models
from django.utils.translation import ugettext as _
import iptools

class IPAddressField(models.Field):
    __metaclass__ = models.SubfieldBase

    description = _("Real IP Address field")

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _('Please enter a valid IP Address (x.x.x.x)'),
        }

    def get_internal_type(self):
        return "IntegerField"

    def to_python(self, value):
        if value is None:
            return value

        elif isinstance(value, str) or isinstance(value, unicode):
            return value

        elif isinstance(value, int) or isinstance(value, long):
            return iptools.long2ip(value)

        assert False, "This should never happen"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value

        elif isinstance(value, str):
            return iptools.ip2long(value)

        elif isinstance(value, int) or isinstance(value, long):
            return value

    def get_prep_lookup(self, lookup_type, value):
        if value is None:
            return value

        elif isinstance(value, str) or isinstance(value, unicode):
            return iptools.ip2long(value)

        elif isinstance(value, int):
            return int

        else:
            assert False, "This should never happen"