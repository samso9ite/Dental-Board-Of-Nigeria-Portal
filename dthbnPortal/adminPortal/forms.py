from django import forms
from schPortal.models import *
from adminPortal.models import IndexLimit, examLimit

class setLimit(forms.ModelForm):
    class Meta:
        model = School
        fields = ('index_quota_limit',)

class createLimit(forms.ModelForm):
    class Meta:
        model = IndexLimit
        fields = ('assigned_limit', )


class setExamLimit(forms.ModelForm):
    class Meta:
        model = examLimit
        fields = ('assigned_limit',)

class UpdateIndexStatus(forms.ModelForm):
    class Meta:
        model = Indexing
        fields = ('approved', 'unapproved', 'comment',)

class UpdateExamStatus(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = ('approved', 'declined', 'comment')