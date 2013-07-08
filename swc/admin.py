from django.contrib import admin
from swc.models import SWCPerson, SWCEvent, Participant


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(SWCPerson, PersonAdmin)


class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(SWCEvent, EventAdmin)
