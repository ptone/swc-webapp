from dateutil.parser import parse

from django.views.generic import ListView, DetailView, UpdateView, View
from django.shortcuts import render

from braces.views import JSONResponseMixin

from .models import SWCEvent, SWCPerson, TimeChunk
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
        return SWCPerson.get_for_user(self.request.user)


class ProfileView(DetailView):
    model = SWCPerson
    fields = ['name1']
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is None:
            return SWCPerson.get_for_user(self.request.user)
        return super(ProfileView, self).get_object()


def calendar(request):
    return render(request, "calendar_test.html", {'target': 'user'})


class AddTimeChunk(JSONResponseMixin, View):
    http_method_names = [u'post']

    def post(self, *args, **kwargs):
        start = parse(self.request.POST.get('start'))
        end = parse(self.request.POST.get('end'))
        create_kwargs = {'start_date': start.date(), 'end_date': end.date()}
        if self.request.POST.get('target') == 'user':
            person = SWCPerson.get_for_user(self.request.user)
            create_kwargs['person'] = person
        elif 'event-' in self.request.POST.get('target'):
            # target specified as 'event-<event pk>'
            pk = self.request.POST.get('target').split('-')[1]
            event = SWCEvent.objects.get(pk=pk)
            create_kwargs['event'] = event
        chunk, created = TimeChunk.objects.get_or_create(**create_kwargs)
        return self.render_json_response({"msg": "OK", "event-id": chunk.id})
