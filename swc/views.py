from django.views.generic import ListView, DetailView

from swc.models import SWCEvent


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
