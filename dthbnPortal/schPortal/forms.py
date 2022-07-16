from django import forms
from schPortal.models import *
from authentication.models import User, Ticket
from cities_light.models import Region
from cities_light.models import Country
from schPortal.choices import *


class schUpdateForm(forms.ModelForm):
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    region = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
   
    class Meta:
        model = School
        fields = ('postal_number', 'phone_number', 'region', 'hod_name', 'hod_phone', 'hod_email','address', 'state', 'sch_logo')

           

class IndexingForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    # religion = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    nationality = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    school_attended1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    school_attended2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    school_attended3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    permanent_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    place_of_work = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    qualification1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    qualification2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    qualification3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    admission_year = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    graduation_year = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    contact_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_name1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_address1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    referee_phone1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_name2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    referee_phone2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    # marriage_cert = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    examination_number1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    examination_year1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    examination_number2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    examination_year2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    referee_phone2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    examination_type1 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_type)
    examination_type2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_type)
    state =  forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=state)
    # sex = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'class':'form-control'}), choices=gender)
    # year = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=year)
    cadre = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=cadre)
    marital_status = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control',  }), choices=marital_status)
    religion = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=religion)
    grade1 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=exam_grade)
    grade2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=exam_grade)
    grade3 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=exam_grade)
    grade4 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control',  }), choices=exam_grade)
    grade5 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control',  }), choices=exam_grade)
    grade6 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    grade7 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    grade1_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    grade2_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control', }), choices=exam_grade)
    grade3_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control',  }), choices=exam_grade)
    grade4_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    grade5_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=exam_grade)
    grade6_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    grade7_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_grade)
    sub1_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub2_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=subject)
    sub3_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=subject)
    sub4_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub5_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub6_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub7_2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub1 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub2 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub3 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub4 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=subject)
    sub5 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control' }), choices=subject)
    sub6 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=subject)
    sub7 = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=subject)
    exam_sitting = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}), choices=exam_sitting)
    
    class Meta:
        model = Indexing
        # fields = "__all__"
        exclude = ('year, institution_id',)


class ExamRegForm(forms.ModelForm):
    residential_country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    residential_state = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    residential_lga = forms.ModelChoiceField(queryset=LGA.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    state_of_origin = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    lga_state = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    state_of_birth = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    lga_of_birth = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    office_country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    office_lga = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    office_state = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-control', 'required':'False'}))
    residential_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    date_of_birth = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    maiden_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    postal_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    religion = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    qualification1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    qualification2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    qualification3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    qualification4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    prof_qualification1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    prof_qualification2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    prof_qualification3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'required':'False'}))
    prof_qualification4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    institution_attended1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    institution_attended2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    institution_attended3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    institution_attended4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    hod_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    hod_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    hod_email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    present_position = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    department = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    office_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    office_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    office_email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    office_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_name1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_phone1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_email1 = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_name2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_phone2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    referee_email2 = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 

    class Meta:
        model = ExamRegistration
        exclude = ('year, institute_id',)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'message', 'department', 'priority', 'subject', 'attachment1', 'attachment2')

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('message', 'attachment1', 'attachment2' )











