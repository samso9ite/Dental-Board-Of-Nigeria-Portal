from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from schPortal.models import *
from schPortal.forms import *
from authentication.forms import *
from authentication.models import Ticket, SubTicket
from cities_light.models import Region
from cities_light.models import Country
from django.urls import reverse_lazy
from authentication.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
import sweetify
import xlwt
from django.urls import reverse
import random
from django.template.defaulttags import register


# Create your views here.

class SchoolProfile(LoginRequiredMixin,CreateView):
    model = School
    form_class = schUpdateForm
    success_url = reverse_lazy('schoolPortal:dashboard')
    template_name = 'school/schools_account_update.html'
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.User = user
        try:
            user = User.objects.get(id=user.id)
            user.profile_update = True
            user.save()
            sweetify.success(request, 'Profile Updated Successfully', button='Great!')
        except user.DoesNotExist:
            sweetify.error(request, 'User Doesn\'t Exist', button='Great!')
        return super().form_valid(form)
       


# def load_cities(request):
#     country_id = request.Get.get('country')
#     print(country_id)
#     region = Region.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'school/schools_account_update.html', {'region': region} )

def load_cities(request):
    country_id = request.Get.get('country')
    print(country_id)
    region = Region.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'school/schools_account_update.html', {'region': region} )


@login_required
def Dashboard(request):
    user = request.user
    school_data = ''
    if user.is_authenticated and user.is_school:
        if user.profile_update:
            school_data = School.objects.get(User=user.id)
       
            exam_reg_stud = ExamRegistration.objects.filter(institute_id=school_data.id).count()
            total_indexed = Indexing.objects.filter(institution_id=request.user).count()
            context =    {
                'school_data': school_data,
                'exam_reg_stud': exam_reg_stud,
                'total_indexed': total_indexed,
            }
            return render(request, "school/Dashboard.html", context)
        else:
           return render(request, "school/Dashboard.html")
    else:
        return HttpResponseRedirect(reverse("Auth:Register"))

@login_required
def AccountUpdate(request, User):
    if request.user.is_authenticated and request.user.is_school:
        sch_update_data = School.objects.get(User=request.user.id)
        school_data = sch_update_data
        context = {}
        form = schUpdateForm(request.POST or None, instance = sch_update_data) 
        if form.is_valid():
            form.save(commit=False)
            updated_at = timezone.now()
            form.save(commit=True)
            sweetify.success(request, 'Profile Updated Successfully', button='Great!')
        return render(request, "school/schools_account_update.html", {'form': form, 'school_data':school_data})  
    else:
        return HttpResponseRedirect(reverse("Auth:Register"))     


# @register.filter
# def selected_labels(SignUp, programme):
#     return [label for value, label in SignUp.fields[programme].choices if value in SignUp[programme].value()]

class NewIndexingView(CreateView):
    model = Indexing
    template_name = "school/add_indexing.html"
    redirect_field_name = reverse_lazy("Auth:Register")
    form_class =  IndexingForm
    success_url = reverse_lazy('schoolPortal:new_indexing')

    def form_valid(self, form) :
        indexed = Indexing.objects.filter(institution=self.request.user.id).count()
        assigned_quota = School.objects.values_list('index_quota_limit', flat=True).get(User_id=self.request.user.id)
        try:
            if indexed == assigned_quota:
                sweetify.success(self.request, "Oops! Limit has been reached", persist='OK')
                return HttpResponseRedirect(reverse("schoolPortal:currentIndex"))
            else:
                form.instance.institution = self.request.user
                sweetify.success(self.request, 'Indexed Successful', button='Great!')
                return super().form_valid(form)
        except:
            pass
      
    
   
class ExamReg(CreateView, LoginRequiredMixin):
    model = ExamRegistration
    form_class = ExamRegForm
    redirect_field_name = reverse_lazy("Auth:Register")
    success_url = reverse_lazy('schoolPortal:exam_reg')
    template_name = 'school/Exam_reg.html'
    
    def form_valid(self, form):
        form.instance.school = self.request.user
        return super().form_valid(form)
    
    

class CurrentIndexing(TemplateView):
    template_name = 'school/current_indexing.html'


@login_required
def IndexListView(request):
    if request.user.is_authenticated and request.user.is_school:
    
        queryset = ''
        if request.path == '/school/current_index':
            queryset = Indexing.objects.filter(institution=request.user).filter(submitted=False)
            
        elif request.path == '/school/indexed_record/':
            queryset  = Indexing.objects.filter(institution=request.user).filter(submitted=True)

        elif request.path == '/school/approved_student/':
            queryset = Indexing.objects.filter(institution=request.user).filter(approved = True)

        elif request.path == '/school/unapproved_student/':
            queryset = Indexing.objects.filter(institution=request.user).filter(unapproved = True, submitted=True)

        else :
            pass
        
    
        page = request.GET.get('page', 1)  
        paginator = Paginator(queryset, 3)

        try:
            indexed = paginator.page(page)
        except PageNotAnInteger:
            indexed = paginator.page(1)
        except EmptyPage:
            indexed = paginator.page(paginator.num_pages)

        return render(request, 'school/indexing_list.html', {'indexed':indexed})
    
    elif request.user.is_authenticated and not request.user.is_school:
        return HttpResponseRedirect(reverse("Auth:Register")) 


@login_required
def ExamListView(request):
    if request.user.is_authenticated and request.user.is_school:
    
        queryset = ''
        sch_id = School.objects.values_list('id', flat=True).get(User_id=request.user)
            
        if request.path == '/school/current_exam_record/':
            queryset = ExamRegistration.objects.filter(institute=sch_id).filter(submitted=False)
        
        elif request.path == '/school/submitted_exam_record/':
            queryset = ExamRegistration.objects.filter(institute=sch_id).filter(submitted=True)

        elif request.path == '/school/approved_exam_record/':
            queryset = ExamRegistration.objects.filter(institute=sch_id).filter(approved=True)

        elif request.path == '/school/declined_exam_record/':
            queryset = ExamRegistration.objects.filter(institute=sch_id).filter(declined=True)
        else:
            pass


        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 1)

        try:
            exam_records = paginator.page(page)
        except PageNotAnInteger :
            exam_records = paginator.page(1)
        except EmptyPage :
            exam_records = paginator.page(paginator.num_pages)


        return render(request, 'school/exam_record_list.html', {'exam_records': exam_records})

    elif request.user.is_authenticated and not request.user.is_school:
        return HttpResponseRedirect(reverse("Auth:Register")) 

@login_required
def edit_index(request, id):
    if request.user.is_authenticated and request.user.is_school:

        index_update_data = Indexing.objects.get(id=id)
        form = IndexingForm(request.POST or None, instance = index_update_data)

        if form.is_valid():
            form.save(commit=False)
            form.instance.institution = request.user
            form.save()
            sweetify.success(request, 'Record updated succesffully', button='Great!')
            return render(request, 'school/add_indexing.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse("Auth:Register")) 

@login_required
def update_exam_record(request, id):
    if request.user.is_authenticated and request.user.is_school:

        exam_record_data = ExamRegistration.objects.filter(id=id)
        form = ExamRegForm(request.POST or None, instance=exam_record_data)

        if form.is_valid() and user.is_school:
            form.save(commit=False)
            form.instance.school = request.user
            form.save()
            sweetify.success(request, 'Record updated succesffully', button='Great!')
            return render(request, 'school/Exam_reg.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse("Auth:Register")) 



@login_required
def delete_record(request, id):
    if '/school/delete_record/' in request.path :
        try :
            record = Indexing.objects.get(id=id)
           
        except Indexing.DoesNotExist:
            pass
        record.delete()
        sweetify.success(request, "Record has been deleted")
        return HttpResponseRedirect(reverse("schoolPortal:currentIndex")) 

    elif '/school/current_exam_record/' in request.path:
        try:
            record = ExamRegistration.objects.get(id)
        except record.DoesNotExist:
            pass
        record.delete()
        return render(request, 'school/exam_record_list.html')

  
@login_required 
def submit_index_record(request):
    records = ''
    
    try :
        records = Indexing.objects.filter(Q(submitted=False), 
        institution_id=request.user.id).update(submitted=True) 
    except Indexing.DoesNotExist:
        sweetify.error(request, 'Record Doesn\'t Exist' , button='Great!')
    return render(request, 'school/indexing_list.html')

@login_required
def submit_exam_record(request):
    records = ''
    try :
        records = ExamRegistration.objects.filter(Q(submitted=False),
         school_id=request.user.id).update(submitted=True)
    except ExamRegistration.DoesNotExist():
        sweetify.error(request, 'Record Doesn\'t Exist' , button='Great!')
    return render(request, 'school/exam_record_list.html')



# Ticket Views
# class Ticket(TemplateView):
#     template_name = 'school/ticket.html'

class ViewTicket(TemplateView):
    template_name = 'school/view_ticket.html'

class CreateTicket(CreateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy("schoolPortal:ticket")
    template_name = "school/ticket.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.ticket_status = 'Open'
        random_num = random.randrange(1000, 10000)
        form.instance.ticket_id = random_num
        form.instance.first_created = True
        sweetify.success(self.request, 'Ticket Created', button='Great!')
        return super().form_valid(form)

@login_required
def ticket_list(request):
    if request.user.is_authenticated and request.user.is_school:
        record = ''
        last_updated_status = []
        last_updated_time = []
        if 'school/all_ticket' in request.path:
            record = Ticket.objects.filter(user_id=request.user.id, first_created=True)
            for last in record:
                last_updated_record = Ticket.objects.filter(ticket_id=last.ticket_id).latest('last_updated')
                last_updated_status.append({last.id:last_updated_record.ticket_status})
                last_updated_time.append({last.id:last_updated_record.last_updated})
              
        elif 'school/answeredticket' in request.path:
            record = Ticket.objects.filter(user_id=request.user.id, ticket_status = 'Answered')

        elif 'school/opened_ticket' in request.path:
            record = Ticket.objects.filter(user_id=request.user.id, ticket_status= 'Open')
           
        elif 'school/closed_ticket' in request.path:
            record = Ticket.objects.filter(user_id=request.user.id, ticket_status= 'Closed')
        else :
            pass

        page = request.GET.get('page', 1)
        paginator = Paginator(record, 5)

        try:
            ticket_list = paginator.page(page)
        
        except PageNotAnInteger:
            ticket_list = paginator.page(1)
        except PageNotAnInteger:
            ticket_list = paginator.page(paginator.num_pages)

        context = {'ticket_list': ticket_list, 'last_updated_status': last_updated_status,
                    'last_updated_time': last_updated_time}
        
        return render(request, 'school/ticket_list.html', context)
    
    else:
        return HttpResponseRedirect(reverse("Auth:Register")) 

@register.filter
def get_item(last_updated_status, key):
    for last_record in last_updated_status or last_record in last_updated_time:
        if key in last_record:
            return last_record.get(key)
        

@login_required
def view_a_ticket(request, id):
    get_record = Ticket.objects.get(id=id)
    record = Ticket.objects.filter(ticket_id=get_record.ticket_id).latest('last_updated')
    all_records = Ticket.objects.filter(ticket_id=get_record.ticket_id).order_by('-id')
    if 'school/update_ticket' in request.path:
        if record.ticket_status != 'Closed':
            form = UpdateTicketForm(request.POST or None)
            if form.is_valid:
                form.save(commit=False)
                form.instance.ticket_id =record.ticket_id
                form.instance.user_id = record.user_id
                form.instance.priority = record.priority
                form.instance.department = record.department
                form.instance.subject = record.department
                form.instance.name = record.name
                form.instance.created_date = record
                form.instance.ticket_status = 'Customer Reply'
                form.save()
                sweetify.success(request, 'Ticket Updated', button='Great!')
            else:
                sweetify.error(request, 'Form is not valid', button='Great!')
        else:
           sweetify.error(request, 'Ticket has been closed', button='Great!') 
    
    elif 'school/close_ticket' in request.path:
        if record.ticket_status !=  'Closed':
            record.ticket_status = 'Closed'
            record.save()
            sweetify.success(request, 'Ticket Closed', button='Great!')
        else:
            sweetify.error(request, "Ticket Status is Closed ")
        
        
    return render(request, 'school/view_ticket.html', {'record': record, 'all_records': all_records})


def export_indexed_stu(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Schools')
    row_num = 0
   
    font_style = xlwt.XFStyle()
    font_style.font.bold = True   
    if '/school/export_indexed_student/xls/' or '/school/export_approved_student/xls/' in request.path: 
        response = HttpResponse(content_type='applicaton/mx-excel')
        if '/school/export_indexed_student/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Indexed Record.xls"'
        elif '/school/export_approved_student/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Approved Student Record.xls"'

        columns = ['First Name', 'Middle Name',  'Surname',  'Cadre', 'Permanent Address', 'Phone Number', 'Email', 
                        'Age', 'State Of Origin', 'Religion', 'Nationality', 'Marital Status', 'School Attended(1)', 'Qualification(1)', 'School Attended(2)', 'Qualification(2)',
                        'School Attended(3)', 'Qualification(3)', 'School Attended(4)', 'Qualification(4)', 'Year of Admission', 
                        'Year of Graduation', 'Contact Address', 'Place of Work', 'Referee Name(1)', 'Referee Address(1)', 'Referee Mobile(1)'
                        'Referee Name(2)', 'Referee Address(2)', 'Referee Mobile(2)',]
            
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet Body, remaining rows
        font_style = xlwt.XFStyle()

        if '/school/export_indexed_student/xls/' in request.path:
        
            rows = Indexing.objects.filter(institution_id=request.user.id, submitted=True).values_list('first_name', 'middle_name', 'surname', 'cadre', 'permanent_address', 'telephone', 'email', 
            'age', 'state', 'religion', 'nationality', 'marital_status', 'school_attended1', 'qualification1', 'school_attended2', 'qualification2',
                'school_attended3', 'qualification3', 'admission_year', 'graduation_year', 'contact_address', 'place_of_work', 
                'referee_name1', 'referee_address1', 'referee_phone1', 'referee_name2', 'referee_address2', 'referee_phone2')

        elif '/school/export_approved_student/xls/' in request.path:
            
            rows = Indexing.objects.filter(institution_id=request.user.id, approved=True).values_list('first_name', 'middle_name', 'surname', 'cadre', 'permanent_address', 'telephone', 'email', 
            'age', 'state', 'religion', 'nationality', 'marital_status', 'school_attended1', 'qualification1', 'school_attended2', 'qualification2',
                'school_attended3', 'qualification3', 'admission_year', 'graduation_year', 'contact_address', 'place_of_work', 
                'referee_name1', 'referee_address1', 'referee_phone1', 'referee_name2', 'referee_address2', 'referee_phone2', )
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def export_exam_record(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Schools')
    row_num = 0
   
    font_style = xlwt.XFStyle()
    font_style.font.bold = True   
    if '/school/export_submitted_exam_record/xls/' or '/school/export_current_exam_record/xls/' in request.path: 
        sch_id = School.objects.values_list('id', flat=True).get(User_id=request.user.id)
        print(sch_id)
        response = HttpResponse(content_type='applicaton/mx-excel')
        if '/school/export_submitted_exam_record/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Submitted Record for Exam.xls"'
        elif '/school/export_current_exam_record/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Current Exam Record.xls"'

        columns = ['Title', 'First Name', 'Middle Name',  'Surname',  'Cadre', 'Address', 'Phone Number', 'Email', 
                    'Date of Birth', 'State of Origin', 'Religion', 'Marital Status', 'Maiden Name', 'Senatorial District', 'Qualification(1)', 'qualification(2)', 'qualification(3)', 'qualification(4)',
                    'Professional Qualification', 'Professional Qualification(2)', 'Professional Qualification(3)', 'Professional Qualification(4)', 'Institution Attended(1)', 'Institution Attended(2)', 'Institution Attended(3)', 'Institution Attended(4)', 'Hod\'s Name', 'Hod\s Phone', 
                    'Hod\s Email','Employment Status', 'Office Name', 'Office Country', 'Office LGA', 
                    'Office Phone Number', 'Office Email', 'Sector', 'Present Position', 'Department', 
        ]
            
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet Body, remaining rows
        font_style = xlwt.XFStyle()

        if '/school/export_submitted_exam_record/xls/' in request.path:
        
            rows = ExamRegistration.objects.filter(institute_id=sch_id, submitted=True).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )
    
        elif '/school/export_current_exam_record/xls/' in request.path:
            
            rows = ExamRegistration.objects.filter(institute_id=sch_id, submitted=False).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )
            
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
