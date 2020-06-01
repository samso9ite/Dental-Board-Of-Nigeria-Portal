from django import forms
from profPortal.models import Professional


class ProfAccntForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    maiden_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    residential_country = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    residential_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    residential_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    residential_lga = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_of_origin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lga_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    senatorial_district = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lga_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    qualification1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SSCE (1990-1993)'}))
    qualification2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: OND/HND/BSC (1995-1998)'}))        
    qualification3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: MSC (1995-1998)'}))
    qualification4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: OTHERS (1995-1998)'}))
    prof_qualification1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SSCE (1990-1993)'}))
    prof_qualification2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: OND/HND/BSC (1995-1998)'}))        
    prof_qualification3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: MSC (1995-1998)'}))
    prof_qualification4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: OTHERS (1995-1998)'}))
    present_position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_lga = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    office_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
     
    class Meta:
        model = Professional
        exclude = ('user',)