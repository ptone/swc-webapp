import datetime

from django.contrib import admin
from swc.models import SWCPerson, SWCEvent, Participant


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(SWCPerson, PersonAdmin)


class ParticipantInline(admin.TabularInline):
    model = Participant
    ordering = ['role', 'person__name1']


class PastPresentFilter(admin.SimpleListFilter):
    title = 'When'
    parameter_name = title.lower()

    def lookups(self, request, model_admin):
        return (
                ('past', "in the past"),
                ('future', "in the future"),
                )

    def queryset(self, request, queryset):
        if self.value() == 'past':
            # note: you can not change order_by here
            return queryset.filter(
                    start_date__lt=datetime.date.today(),
                    )
        if self.value() == 'future':
            return queryset.filter(
                    start_date__gte=datetime.date.today(),
                    )
        return queryset


class EventAdmin(admin.ModelAdmin):
    # TODO set reg actions
    date_hierarchy = 'start_date'
    list_display = ['venue', 'start_date', 'registration']
    list_editable = ['registration']
    list_filter = ['type', 'registration', PastPresentFilter]
    inlines = [ParticipantInline]

    def get_ordering(self, request):
        """
        we override this to provide reverse chrono sort
        on past events
        """
        ordering = super(EventAdmin, self).get_ordering(request)
        if request.GET.get('when', False) == 'past':
            ordering = [field for field in ordering if
                    'start_date' not in field]
            ordering.append('-start_date')
        return ordering

admin.site.register(SWCEvent, EventAdmin)
