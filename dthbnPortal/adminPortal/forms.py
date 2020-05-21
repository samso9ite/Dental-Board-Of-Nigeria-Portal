from django import forms
from schPortal.models import *

class setLimit(forms.ModelForm):
    class Meta:
        model = School
        fields = ('index_quota_limit',)


class setExamLimit(forms.ModelForm):
    class Meta:
        model = School
        fields = ('exam_quota_limit',)

class UpdateIndexStatus(forms.ModelForm):
    class Meta:
        model = Indexing
        fields = ('approved', 'unapproved', 'comment',)

class UpdateExamStatus(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = ('approved', 'declined', 'comment')