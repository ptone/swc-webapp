from __future__ import unicode_literals

import datetime

from django.db import models

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices


@python_2_unicode_compatible
class SWCPerson(models.Model):
    user = models.OneToOneField(User, related_name="profile", null=True,
            blank=True)
    name1 = models.CharField(max_length=80)
    name2 = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    # location
    # organizational affiliation
    contact_phone = models.TextField(blank=True)
    profile_email = models.EmailField(max_length=254, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return "{} {}".format(self.name1, self.name2)


class UpcomingEventManager(models.Manager):
    def get_queryset(self):
        return super(UpcomingEventManager, self).get_queryset().filter(
                start_date__gte=datetime.date.today())


class OpenEventsManager(UpcomingEventManager):
    def get_queryset(self):
        return super(OpenEventsManager, self).get_queryset().filter(
                registration='open')


@python_2_unicode_compatible
class SWCEvent(models.Model):
    TYPES = Choices('bootcamp', 'training')
    REGISTRATIONS = Choices('open', 'restricted', 'full', 'pending', 'closed')

    type = models.CharField(choices=TYPES, default=TYPES.bootcamp,
            max_length=50)
    # location
    start_date = models.DateField()
    end_date = models.DateField()
    human_times = models.CharField(verbose_name="Event Times",
            default="9AM to 4:30PM", max_length=50)
    venue = models.TextField(blank=True)
    registration = models.CharField(choices=REGISTRATIONS,
            default=REGISTRATIONS.pending, max_length=40)
    capacity = models.IntegerField(default=40)
    home_page = models.URLField(blank=True)
    participants = models.ManyToManyField(SWCPerson, through='Participant')

    objects = models.Manager()
    upcoming = UpcomingEventManager()
    open = OpenEventsManager()

    class Meta:
        unique_together = (("start_date", "venue"),)

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
        return '-'.join(self.event, self.person, self.role)

# TODO Badge
