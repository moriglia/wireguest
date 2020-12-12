import ldap
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI = "ldap://ldap.mydomain.com"

AUTH_LDAP_BIND_DN = ""
AUTH_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=users,o=mydomain,c=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)
