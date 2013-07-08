import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_info(path=os.path.join(BASE_DIR, '_config.yml')):
    # import pdb; pdb.set_trace()
    with open(path, 'r') as reader:
        return yaml.load(reader)

bc_config = load_info()

BOOTCAMP_CONFIG_KEYS = [
    'contact',
    'facebook_url',
    'github_url',
    'google_plus_url',
    'rss_url',
    'twitter_name',
    'twitter_url'
]


def swc_context(request):
    """
    A template context processor to add site meta from main site
    """
    site = {}
    page = {'shared': '/static', 'root': '/static'}
    for key in BOOTCAMP_CONFIG_KEYS:
        site[key] = bc_config[key]
    return {'site': site, 'page': page}
