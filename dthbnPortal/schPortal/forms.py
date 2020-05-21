from django import forms
from schPortal.models import *
from authentication.models import User, Ticket
from cities_light.models import Region
from cities_light.models import Country


class schUpdateForm(forms.ModelForm):
    # region = forms.Model.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    # programme = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=User.cadre_choices)
    class Meta:
        model = School
        fields = ('postal_number', 'phone_number', 'region', 'country', 'hod_name', 'hod_phone', 'hod_email','address', 'sch_logo')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'country' in self.data:
                try:
                    country_id = int(self.data.get('country'))
                    self.fields['region'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.country.region_set.order_by('name')


class IndexingForm(forms.ModelForm):
    class Meta:
        model = Indexing
        fields = "__all__"


class ExamRegForm(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = "__all__"

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'message', 'department', 'priority', 'subject', 'attachment1', 'attachment2')

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('message', 'attachment1', 'attachment2' )











