from .dev import *
from subprocess import check_output

SITE_URL = check_output('curl http://pytohost.com/ip.php').strip()
