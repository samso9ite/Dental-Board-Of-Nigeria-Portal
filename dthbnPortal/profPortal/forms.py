from django import forms
from profPortal.models import Professional


class ProfAccntForm(forms.ModelForm):
    
     
    class Meta:
        model = Professional
        exclude = ('profuser',)