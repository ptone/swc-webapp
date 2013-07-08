import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")

from pyquery import PyQuery as pq
import glob
import re

from swc.models import SWCPerson

people_path = '/Users/preston/Projects/swc/new-site/site/bc/_includes/people/*.html'

people_files = glob.glob(people_path)

SWCPerson.objects.all().delete()

i = 0
for f in people_files:
    i += 1
    # with open(f, 'r') as handle:
        # data = handle.read()
    try:
        page = pq(filename=f)
        person_element = page('.person')
    except AttributeError as e:
        print f
    if person_element:
        person_name = person_element.text().replace('\n', '')
        person_name = re.sub(' +', ' ', person_name)
        names = person_name.split()

        name1 = names[0]
        name2 = ''
        if len(names) > 1:
            name2 = ' '.join(names[1:])

        # TODO bio and email
        SWCPerson.objects.create(
                name1=name1,
                name2=name2,
                profile_email='emailfoo %s' % i
                )
