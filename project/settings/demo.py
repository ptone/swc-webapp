from .dev import *

from subprocess import check_output

SITE_URL = "http://{}".format(
        check_output('curl http://pytohost.com/ip.php', shell=True).strip()
        )
