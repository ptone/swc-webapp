from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from .models import SWCEvent, SWCPerson
from .forms import ProfileForm


class EventList(ListView):
    model = SWCEvent
    template_name = 'bootcamp_list.html'


class UpcomingBootcamps(EventList):
    def get_queryset(self):
        return self.model.upcoming.filter(type='bootcamp')


class EventDetail(DetailView):
    model = SWCEvent
    context_object_name = 'event'
    template_name = "event_detail.html"

# note login_required applied at URL
class EditProfile(UpdateView):
    model = SWCPerson
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'

    def get_object(self):
        obj, created = SWCPerson.objects.get_or_create(user=self.request.user,
                defaults={'profile_email': self.request.user.email})
        return obj


class ProfileView(DetailView):
    model = SWCPerson
    fields = ['name1']
    template_name = 'profile_detail.html'
    context_object_name = 'profile'
