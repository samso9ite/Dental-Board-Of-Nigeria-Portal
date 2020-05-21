from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from authentication.forms import SignUp, ProfSignUp, LoginForm, ChangePasswordForm
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from authentication.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from authentication.models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from schPortal import urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
import sweetify
# Create your views here


def sign_up_view(request):
    if request.user.is_authenticated:
        HttpResponseRedirect('/')
    if request.method == 'POST' and 'is_school' in request.POST:
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            subject = 'Account Activation Link'
            message = render_to_string('auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('Auth:account_activation_sent')
    else:
        form = SignUp()
   
    if request.method == 'POST' and 'is_professional' in request.POST:
        prof_form = SignUp(request.POST)
        if prof_form.is_valid():
            print("professional FORM IS VALID")
            user = prof_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            subject = 'Account Activation Link'
            message = render_to_string('auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('Auth:account_activation_sent')
    else:
        prof_form = ProfSignUp()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            try:
                get_user_name = User.objects.get(email=email)
                user = authenticate(username=get_user_name, password=password)
                if user and user.is_active and user.suspend is False and user.block is False:
                    login(request, user)
                    if User.objects.filter(email=user.email).filter(is_school=True).filter(profile_update="False"):
                        sweetify.success(request, 'Login Successful', button='Great!')
                        return redirect("schoolPortal:schoolProfile")

                    elif User.objects.filter(email=user.email).filter(is_school=True).filter(profile_update="True"):
                        sweetify.success(request, 'Login Successful', button='Great!')
                        return redirect("schoolPortal:dashboard")
    
                    elif User.objects.filter(email=user.email).filter(is_professional=True):
                        return HttpResponse('Logged in Professional')

                    elif User.objects.filter(email=user.email).filter(is_admin=True):
                        sweetify.success(request, 'Login Successful', button='Great!')
                        return redirect('adminPortal:dashboard')

                elif user and user.is_active and user.suspend is True and user.block is False:
                    sweetify.error(request, 'School Has Been Suspended', text='Contact the board for more details', button='Great!')
                    return HttpResponseRedirect(reverse("Auth:Register"))

                elif user and user.is_active and user.suspend is False and user.block is True:
                    sweetify.error(request, 'School Has Been Blocked', text='Contact the board for more details', button='Great!')
                    return HttpResponseRedirect(reverse("Auth:Register"))
                else:
                    sweetify.error(request, 'Invalid Username or Password')
                    return HttpResponseRedirect(reverse("Auth:Register"))
            except:
                sweetify.success(request, 'Invalid Username or Password')
                return HttpResponseRedirect(reverse("Auth:Register"))
    else:
        login_form = LoginForm()
    return render(request, 'auth/sch_register.html',
                  {'form': form, 'prof_form': prof_form, 'login_form': login_form})


def account_activation_sent(request):
    return render(request, 'auth/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.reset = True
        if user.is_school:
            SchoolCode.objects.filter(reg_number=user.code).update(used=True, user_id=user.id)
            user.save()
            login(request, user)
            return redirect('schoolPortal:schoolProfile',)
       
      
    else:
        return render(request, 'auth/sch_registration.html')


@login_required
def logout_view(request):
    logout(request)
    sweetify.success(request, 'Log  Successfully', button='Great!')
    return redirect("Auth:Register")


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Your password has been reset')
            sweetify.success(request, 'Password Changed Successfully')
                
            if user.is_school:
                return HttpResponseRedirect(reverse("schoolPortal:dashboard"))
            elif user.is_professional:
               return HttpResponse("Password for professional Chanegd")
            elif user.is_admin:
                return HttpResponse("Password changed for admin")
       
    else:
        form = PasswordChangeForm(request.user)
    if request.user.is_school:
        return render(request, 'school/change_password.html', {"form":form})
    elif request.user.is_admin:
        return render(request, 'adminPortal/change_password.html', {'form':form})
    else:
        pass

# class SweetAlert (TemplateView):
#     sweetify.sweetalert(request, 'Westworld is awesome', text='Really... if you have the chance - watch it!')
#     template_name = 'auth/forgot_password.html'

@login_required
def block(request, id):
    try:
        user_instance = User.objects.get(id=id).update(block=True)
    except User.DoesNotExist:
        print("User Does Not Exist")
    return render(request, 'adminPortal/accredited.html')