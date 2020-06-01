from authentication.models import User, SchoolCode, ProfessionalCode
    # from django.forms import ModelForm
from django import forms
from authentication.choices import *
from django.db.models import Q


class SignUp(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School Code'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School Name'}))
    # professional_code = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Registration Code'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))
    # is_school = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    programme = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=User.cadre_choices)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password', 'programme', 'code', 'is_school')

    def clean(self):
        cleaned_data = super(SignUp, self).clean()
        password = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        code = cleaned_data.get("code")

        if password != confirm_pwd:
            self.add_error('confirm_password', "Password doesn't match")

        try:
            if User.objects.filter(email=email):
                self.add_error('email', "Email already exist")

        except User.DoesNotExist:
            pass

        try:
            if SchoolCode.objects.filter(reg_number=code).exists():
                if SchoolCode.objects.filter(reg_number=code).filter(used=True):
                    self.add_error('code', "School code already has been used ")
                elif SchoolCode.objects.filter(reg_number=code).filter(used=False):
                    # SchoolCode.objects.filter(reg_number=code).update(used=True)
                    pass
            # elif SchoolCode.objects.get()
            else:
                self.add_error('code', "Please confirm if the code is correct")
        except SchoolCode.DoesNotExist:
            self.add_error('code', "Doesn't Exist")

        def selected_programme(self):
            return [label for value, label in self.fields['programme'].choices if value in self['programme'].value()]


class ProfSignUp(forms.ModelForm):
    programme = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=User.cadre_choices)
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration Code'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))
    # programme = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=User.cadre_choices,)

    class Meta:
        model = User
        fields = ('code', 'email', 'password', 'programme', 'is_professional')

    def clean(self):
        cleaned_data = super(ProfSignUp, self).clean()
        password = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        code = cleaned_data.get("code")
        programme = cleaned_data.get("programme")
        print(password, confirm_pwd, email, code, programme)

        if password != confirm_pwd:
            raise forms.ValidationError("Password doesn't match")
            print('Password dont match')

        elif email == User.objects.filter(email="email"):
            raise forms.ValidationError("Email has been used")
            print('Email has been used')
        
        try:
            prof_code = ProfessionalCode.objects.get(Q(reg_number=code) & Q(cadre=programme))
            if prof_code:
                print(prof_code.id)
                if prof_code.used is True:
                    self.add_error('code', "Professional code already has been used ")
                    print("Code has been used")
                # elif prof_code.used is False:
                #     pass
            else:
                self.add_error('code', "Please confirm if the code is correct")
        except ProfessionalCode.DoesNotExist:
            self.add_error('code', "Please confirm if the code is correct")
            print('Code incorrect')





class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')

class ChangePasswordForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('password',)

