from django.views.generic.list import ListView

from swc.models import SWCEvent

class EventList(ListView):

    model = SWCEvent
    template_name = 'bootcamp_list.html'

class UpcomingBootcamps(EventList):
    def get_queryset(self):
        return self.model.upcoming.all()

