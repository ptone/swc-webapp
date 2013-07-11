import json
import jingo.monkey
jingo.monkey.patch()
from django import forms
from .models import SWCPerson


class ProfileForm(forms.ModelForm):
    new_geo = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = SWCPerson
        fields = ['name1', 'name2', 'bio', 'profile_email']
        labels = {
                'name1': "First/Given Name",
                'name2': "Last/Family/Surname Names",
                }

    class Media:
        js = ['https://maps.googleapis.com/maps/api/js?sensor=false',
                'js/bootstrap/bootstrap-typeahead.js',
                'js/jquery.addresspicker.js',
                'js/jquery.json-2.4.min.js',
             ]

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(ProfileForm, self).save(commit=False)
        if self.cleaned_data['new_geo']:
            m.geodata = json.loads(self.cleaned_data['new_geo'])
            # TODO extract fields from this blob
            m.geo_type = m.geodata['geometry']['location_type']
            m.lat = m.geodata['lat_val']
            m.long = m.geodata['long_val']
        if commit:
            m.save()
        return m
