from django.db import models

from django.contrib.auth.models import User

from model_utils import Choices

# Create your models here.


class SWCPerson(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    bio = models.TextField(blank=True)
    # location
    # organizational affiliation
    contact_phone = models.TextField(blank=True)


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

# TODO Badge
