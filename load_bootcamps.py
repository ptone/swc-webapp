import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")

import glob

import yaml
from django.db.utils import IntegrityError


def harvest(filespec):
    '''
    Get content and metadata from HTML files. Return a single metadata
    dictionary if a single path is given as input, or a dictionary
    mapping filenames to metadata dictionaries if multiple paths are
    given.
    '''
    if isinstance(filespec, basestring):
        return harvest_single(filespec)

    elif isinstance(filespec, list):
        return dict([(f, harvest_single(f)) for f in filespec])

    else:
        assert False, 'Unknown filespec "{0}"'.format(filespec)


def harvest_single(filename):
    '''Harvest metadata from a single file.'''

    with open(filename, 'r') as reader:
        text = reader.read()
        stuff = text.split('---')[1]
        meta_dict = yaml.load(stuff)
        meta_dict['path'] = filename
        return meta_dict

bootcamp_path = '/Users/preston/Projects/swc/new-site/site/bootcamps/'
pages = glob.glob('{}*/index.html'.format(bootcamp_path))

metadata = harvest(pages)
bootcamps = []
for f in metadata:
    bootcamps.append(metadata[f])
    bootcamps[-1]['slug'] = f.split('/')[1]
    if 'contact' not in metadata[f]:  # FIXME: need to figure out how to
    # handle missing in templates
        metadata[f]['contact'] = None
bootcamps.sort(lambda x, y: cmp(x['slug'], y['slug']))



from swc.models import SWCEvent

# {'startdate': datetime.date(2013, 4, 27), 'humantime': '9:00 am - 4:30 pm', 'layout': 'bootcamp', 'shared': '..', 
# 'latlng': '39.291389,-76.625', 'registration': 'open', 'venue': 'University of Maryland, Baltimore',
# 'humandate': 'April 27-28, 2013', 'contact': None, 'eventbrite': 5919069095,
# 'address': 'N111, Pharmacy Hall', 'enddate': datetime.date(2013, 4, 28),
# 'path': '/Users/preston/Projects/swc/new-site/site/bootcamps/2013-04-27-umaryland/index.html',
# 'instructor': ['Azalee Bostroem', 'Alex Viana'], 'slug': 'Users'} # nopep8
#

# flush
SWCEvent.objects.all().delete()

for b in bootcamps:
    try:
        SWCEvent.objects.create(
                start_date=b['startdate'],
                end_date=b['startdate'] + datetime.timedelta(days=2),
                human_times=b.get('humantime', ''),
                registration=b['registration'],
                venue=b['venue']
                )
    except IntegrityError as e:
        print b
