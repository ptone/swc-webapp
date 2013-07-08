from django.contrib import admin
from swc.models import SWCPerson, SWCEvent, Participant


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(SWCPerson, PersonAdmin)

class ParticipantInline(admin.TabularInline):
    model = Participant

class EventAdmin(admin.ModelAdmin):
    # TODO set reg actions
    date_hierarchy = 'start_date'
    list_display = ['venue', 'start_date', 'registration']
    list_editable = ['registration']
    list_filter = ['registration']
    inlines = [ParticipantInline]
admin.site.register(SWCEvent, EventAdmin)
