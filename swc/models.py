from __future__ import unicode_literals

import datetime

from django.db import models

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

from jsonfield import JSONField
from model_utils import Choices
from model_utils.managers import QueryManager


class GeoLocation(models.Model):
    """
    An abstract class to house geographic info
    """
    # raw geocode data from google API
    geodata = JSONField()
    country = models.CharField(max_length=50, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    # the google geocode type resolution
    geo_type = models.CharField(max_length=40, blank=True)
    # the SWC notion of bootcamp regions, determined from country
    region = models.CharField(max_length=40, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SWCPerson(GeoLocation):
    user = models.OneToOneField(User, related_name="profile", null=True,
            blank=True)
    name1 = models.CharField(max_length=80)
    name2 = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    # location
    # organizational affiliation
    # contact_phone = models.TextField(blank=True)
    profile_email = models.EmailField(max_length=254, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return "{} {}".format(self.name1, self.name2)

    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'pk': self.id})

    @property
    def email(self):
        if self.profile_email:
            return self.profile_email
        if self.user and self.user.email:
            return self.user.email
        return None


@python_2_unicode_compatible
class SWCEvent(GeoLocation):
    TYPES = Choices('bootcamp', 'training')
    REGISTRATIONS = Choices(
            'open',
            'restricted',
            'full',
            'pending',
            'closed',
            'proposed',
            )

    type = models.CharField(choices=TYPES, default=TYPES.bootcamp,
            max_length=50)
    # location
    start_date = models.DateField()
    end_date = models.DateField()
    human_times = models.CharField(verbose_name="Event Times",
            default="9AM to 4:30PM", max_length=50)
    venue = models.TextField(blank=True)
    registration = models.CharField(choices=REGISTRATIONS,
            default=REGISTRATIONS.proposed, max_length=40)
    capacity = models.IntegerField(default=40)
    home_page = models.URLField(blank=True)
    participants = models.ManyToManyField(SWCPerson, through='Participant')

    objects = models.Manager()
    upcoming = QueryManager(start_date__gte=datetime.date.today())
    open = QueryManager(
            start_date__gte=datetime.date.today(),
            registration='open',
            )

    @property
    def slug(self):
        return self.__str__()

    class Meta:
        unique_together = (("start_date", "venue"),)
        ordering = ['start_date']

    def __str__(self):
        return "{}-{}".format(self.start_date, self.venue)


@python_2_unicode_compatible
class Participant(models.Model):
    ROLES = Choices('instructor', 'helper', 'host', 'student')
    event = models.ForeignKey(SWCEvent)
    person = models.ForeignKey(SWCPerson, related_name='participation_set')
    role = models.CharField(choices=ROLES, default=ROLES.student,
            max_length=40)
    # confirmed can be used to track whether the participant affirmed a
    # reminder sent x days before event
    confirmed = models.BooleanField(default=False,
            help_text="Has the participant verified they will be attending?")
    attended = models.BooleanField(default=False,
            help_text="Did the participant show up?")
    completed = models.BooleanField(default=False,
            help_text="Did the participant remain and complete the event?")

    def __str__(self):
        return '{}-{}-{}'.format(self.event, self.person, self.role)

# TODO Badge
