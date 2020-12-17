#include <ldap.h>

import ldap
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI = LDAP_URI

AUTH_LDAP_BIND_DN = LDAP_BIND_DN
AUTH_BIND_PASSWORD = LDAP_BIND_PASSWORD
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    LDAP_USER_SEARCH, ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)
