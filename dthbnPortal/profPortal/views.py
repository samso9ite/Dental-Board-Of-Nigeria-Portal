from django.shortcuts import render
from django.views.generic import TemplateView , CreateView, UpdateView
from profPortal.forms import  ProfAccntForm
from profPortal.models import Professional
from django.urls import reverse_lazy

# Create your views here

class Profile(TemplateView):
    template_name = 'profPortal/Dashboard.html'

class Update(TemplateView):
    template_name = 'profPortal/Add.html'

class ProfAccntView(CreateView):
    model = Professional
    template_name = 'profPortal/create.html'
    form_class = ProfAccntForm
    success_url = reverse_lazy('profPortal:dashboard')

    def form_valid(self, form):
        print('form is valid')
        # user = self.request.user
        form.instance.profuser = self.request.user
        form.save()
        print(form.errors)
        return super().form_valid(form)

class ProfAccntUpdateView(UpdateView):
    model = Professional
    template_name = 'profPortal/Add.html'
    form_class = ProfAccntForm
    success_url = reverse_lazy('profPortal:dashboard')
    context_object_name = 'profUpdate'
