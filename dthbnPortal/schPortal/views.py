from cmath import log
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, View
from schPortal.models import *
from schPortal.forms import *
from authentication.forms import *
from authentication.models import Ticket, SubTicket
from cities_light.models import Region, Country
from django.urls import reverse_lazy, reverse
from authentication.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from adminPortal.models import *
import xlwt, random, sweetify
from django.template.defaulttags import register
# from adminPortal.render import Render
from django_xhtml2pdf.utils import generate_pdf
from django_xhtml2pdf.views import PdfMixin


class Pdf(View):
    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        if '/school/indexing/pdf' in request.path:
            record = Indexing.objects.get(institution_id=request.user, id=slug)
        elif '/school/exam/pdf' in request.path:
           record = ExamReg.objects.get(institute_id=request.user, id=slug)
        context_dict = {
            'record': record,
            'request': request
        }
        if '/school/indexing/pdf' in request.path:
            return Render.render('school/indexing_pdf.html', context_dict)
        elif '/school/exam/pdf' in request.path:
            return Render.render('school/exam_pdf.html', context_dict)


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
            sweetify.success(self.request, 'Profile Updated Successfully', button='Great!')
        except user.DoesNotExist:
            sweetify.error(self.request, 'User Doesn\'t Exist', button='Great!')
        return super().form_valid(form)
       
       
def load_cities(request):
    country_id = request.GET.get('residential_country')
    region = Region.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'school/dropdown_list.html', {'region': region} )

def load_office_cities(request):
    country_id = request.GET.get('office_country')
    region = Region.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'school/office_cities.html', {'region': region} )

def load_lga(request):
    state_id = request.GET.get('residential_state')
    lga = LGA.objects.filter(region_id=state_id)
    return render(request, 'school/lga_dropdown.html', {'lga': lga} )

def load_office_lga(request):
    state_id = request.GET.get('office_state')
    lga = LGA.objects.filter(region_id=state_id)
    return render(request, 'school/office_lga.html', {'lga': lga} )


def load_state(request):
    state_id = request.GET.get('state_of_origin')
    print(state_id)
    lga = LGA.objects.filter(region_id=state_id)
    return render(request, 'school/state_dropdown.html', {'lga': lga} )

def load_state_origin(request):
    state_id = request.GET.get('state_of_birth')
    lga = LGA.objects.filter(region_id=state_id)
    return render(request, 'school/origin.html', {'lga': lga} )


@login_required
def Dashboard(request):
    user = request.user
    school_data = ''
    if user.is_authenticated and user.is_school:
        if user.profile_update:
            school_data = School.objects.get(User=user.id)
       
            exam_reg_stud = ExamRegistration.objects.filter(institute_id=school_data.id).count()
            total_indexed = Indexing.objects.filter(institution_id=request.user).count()
            notification = Ticket.objects.filter(Q(ticket_status='Answered') & Q(notification=False)).count()
   
            context =    {
                'school_data': school_data,
                'exam_reg_stud': exam_reg_stud,
                'total_indexed': total_indexed,
                'notification' : notification,
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


class NewIndexingView(CreateView):
    model = Indexing
    template_name = "school/add_indexing.html"
    redirect_field_name = reverse_lazy("Auth:Register")
    form_class =  IndexingForm
    success_url = reverse_lazy('schoolPortal:new_indexing')

    def form_valid(self, form) :
        school_instance = School.objects.get(User_id=self.request.user.id)
        form.instance.year="2021-2022"
        form.instance.institution_id = self.request.user.id
        indexing_status = closeIndexing.objects.filter(id=1)    
        for obj in indexing_status:
           
            indexing_state = obj.access
            if indexing_state is False:
                current_year = datetime.datetime.now().year
                nxt_year = current_year + 1
                # year = str(current_year) + "-" + str(nxt_year) 
                year ="2021-2022"
                indexed = Indexing.objects.filter(institution_id=self.request.user.id, year=year).count()
                assigned= IndexLimit.objects.get(school=school_instance.id, year=year)
                assigned_quota = assigned.assigned_limit  
                try:
                   
                    if indexed is not 0:
                        if assigned_quota:
                            if indexed  == int(assigned_quota):
                                sweetify.error(self.request, "Oops! Limit has been reached", persist='OK')
                                return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
                            else:
                                form.instance.institution_id = self.request.user.id
                                form.save()
                                sweetify.success(self.request, 'Indexed Successful', button='Great!')
                                return super().form_valid(form)
                                
                        else:
                            sweetify.error(self.request, "Oops! Contact the board limit has not been set ", persist='OK')
                            return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
                    elif indexed is 0 and assigned_quota:
                        form.instance.institution_id = self.request.user.id
                        form.save()
                        sweetify.success(self.request, 'Indexed Successful', button='Great!')
                        return super().form_valid(form)
                except:
                    pass
            else:
                sweetify.error(self.request, "Indexing Closed", persist='OK')
                return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
        return HttpResponseRedirect(reverse_lazy('schoolPortal:new_indexing'))


@login_required
def create_exam_record(request):
    if request.user.is_authenticated and request.user.is_school:
        school_instance = School.objects.get(User_id=request.user.id)
        exam_status = closeExamRegistration.objects.filter(id=1)
        # if request.method == "POST":
        for obj in exam_status:
            exam_state = obj.access
            if exam_state is False:
                current_year = datetime.datetime.now().year
                nxt_year = current_year + 1
                last_year = current_year - 1 
                year = str(last_year) + "-" + str(current_year)
                print(year)
                print(request.user.id)
                print(school_instance)
                registered = ExamRegistration.objects.filter(institute_id=request.user.id, year=year).count()
                assigned_quota = examLimit.objects.values_list('assigned_limit', flat=True).get(school=school_instance.id, year=year)
                print(assigned_quota)
                if request.method == "POST":
                    form = ExamRegForm(request.POST or None)
                    try:
                        if registered != 0:
                            if assigned_quota:
                                if registered  == int(assigned_quota):
                                    sweetify.error(request, "Oops! Limit has been reached", persist='OK')
                                    return(HttpResponseRedirect(request.META['HTTP_REFERER']))
                                else:
                                    if form.is_valid():
                                        form.save(commit=False)
                                        form.instance.institute_id = request.user.id
                                        print(form.instance.institute_id)
                                        form.instance.year = year
                                        print(form.instance.year)
                                        form.save()
                                        sweetify.success(request, 'Exam registration Successful', button='Great!')
                                        # return(HttpResponseRedirect(request.META['HTTP_REFERER']))
                                        return render(request, "school/Exam_reg.html") 
                
                            else:
                                sweetify.error(request, "Oops! Contact the board limit has not been set ", persist='OK')
                                return(HttpResponseRedirect(request.META['HTTP_REFERER']))
                        elif registered == 0 and assigned_quota:
                            if form.is_valid():
                                form.save(commit=False)
                                form.instance.institute_id = request.user.id
                                form.instance.year = year
                                form.save(commit=True)
                                print(form)
                                sweetify.success(request, 'Registration Successful', button='Great!')
                                return render(request, "school/Exam_reg.html")
                        
                    except:
                        pass
            else:
                sweetify.error(request, 'Exam Registraton Closed', button='Great!')
                return(HttpResponseRedirect(request.META['HTTP_REFERER']))
        return HttpResponseRedirect(reverse_lazy('schoolPortal:new_exam'))
    def get_context_data(self, **kwargs):
        country_data = Country.objects.all()
        state_data = Region.objects.all()
        lga_data = LGA.objects.all()
        ctx =  super(ExamReg, self).get_context_data(**kwargs)
        ctx['countries'] = country_data
        ctx['state'] = state_data
        ctx['lga'] = lga_data
        return ctx
        
   
class ExamReg(CreateView, LoginRequiredMixin):
    model = ExamRegistration
    form_class = ExamRegForm
    redirect_field_name = reverse_lazy("Auth:Register")
    success_url = reverse_lazy('schoolPortal:exam_reg')
    template_name = 'school/Exam_reg.html'
 
    def form_valid(self, form):
        # print(form)
        school_instance = School.objects.get(User_id=self.request.user.id)
        exam_status = closeExamRegistration.objects.filter(id=1)
        for obj in exam_status:
            exam_state = obj.access
            if exam_state is False:
                current_year = datetime.datetime.now().year
                nxt_year = current_year + 1
                last_year = current_year - 1 
                year = str(last_year) + "-" + str(current_year)
                registered = ExamRegistration.objects.filter(institute_id=self.request.user.id, year=year).count()
                assigned_quota = examLimit.objects.values_list('assigned_limit', flat=True).get(school=school_instance.id, year=year)
                try:
                    if registered != 0:
                        if assigned_quota:
                            if registered  == int(assigned_quota):
                                sweetify.error(self.request, "Oops! Limit has been reached", persist='OK')
                                return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
                            else:
                                form.instance.institute_id = self.request.user.id
                                form.instance.year = year
                                sweetify.success(self.request, 'Exam registration Successful', button='Great!')
                                return super().form_valid(form)
            
                        else:
                            sweetify.error(self.request, "Oops! Contact the board limit has not been set ", persist='OK')
                            return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
                    elif registered == 0 and assigned_quota:
                        form.instance.institute_id = self.request.user.id
                        form.instance.year = year
                        sweetify.success(self.request, 'Registration Successful', button='Great!')
                        return super().form_valid(form)
                    
                except:
                    pass
            else:
                sweetify.error(self.request, 'Exam Registraton Closed', button='Great!')
                return(HttpResponseRedirect(self.request.META['HTTP_REFERER']))
        return HttpResponseRedirect(reverse_lazy('schoolPortal:exam_reg'))


    def get_context_data(self, **kwargs):
        country_data = Country.objects.all()
        state_data = Region.objects.all()
        lga_data = LGA.objects.all()
        ctx =  super(ExamReg, self).get_context_data(**kwargs)
        ctx['countries'] = country_data
        ctx['state'] = state_data
        ctx['lga'] = lga_data
        return ctx
    

class CurrentIndexing(TemplateView):
    template_name = 'school/current_indexing.html'


@login_required
def IndexListView(request, year):
    if request.user.is_authenticated and request.user.is_school:
        queryset = ''
        total_indexed = ''
        total_unapproved = ''
        total_approved = ''
        currentIndex_total = ''
        close_query = ''
       
        if '/school/current_index' in request.path:
            queryset = Indexing.objects.filter(institution_id=request.user,submitted=False, year=year)
            queryset.filter()
            currentIndex_total =Indexing.objects.filter(institution=request.user.id,submitted=False, year=year).count()
        elif '/school/indexed_record/' in request.path:
            queryset  = Indexing.objects.filter(institution=request.user, submitted=True, year=year)
            total_indexed = Indexing.objects.filter(institution=request.user, submitted=True, year=year).count()
        elif '/school/approved_student/' in request.path:
            queryset = Indexing.objects.filter(institution=request.user).filter(approved = True, year=year)
            total_approved = Indexing.objects.filter(institution=request.user).filter(approved = True, year=year).count()
        elif '/school/unapproved_student/' in request.path:
            queryset = Indexing.objects.filter(institution=request.user).filter(unapproved = True, submitted=True, year=year)
            total_unapproved = Indexing.objects.filter(institution=request.user).filter(unapproved = True, submitted=True, year=year).count()
        else :
            pass
        page = request.GET.get('page', 1)  
        paginator = Paginator(queryset, 10000)

        try:
            indexed = paginator.page(page)
        except PageNotAnInteger:
            indexed = paginator.page(1)
        except EmptyPage:
            indexed = paginator.page(paginator.num_pages)
        context = {'currentIndex_total': currentIndex_total, 'close_query':close_query, 'total_indexed': total_indexed, 'total_unapproved': total_unapproved
                    ,'total_approved': total_approved, 'indexed': indexed, 'year':year,}
                    
        return render(request, 'school/indexing_list.html', context)
    
    elif request.user.is_authenticated and not request.user.is_school:
        return HttpResponseRedirect(reverse("Auth:Register")) 

@login_required
def ExamListView(request, year):
    if request.user.is_authenticated and request.user.is_school:
        queryset = ''
        currentExam_total = ''
        total_exam_submitted = ''
        total_exam_approved = ''
        total_exam_declined = ''
        close_query = ''
             
        if '/school/current_exam_record/' in request.path:
            queryset = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(submitted=False)
            currentExam_total = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(submitted=False).count()
            close_query = School.objects.get(User_id=request.user)
        elif '/school/submitted_exam_record/'  in request.path:
            queryset = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(submitted=True)
            total_exam_submitted =  ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(submitted=True).count()
        elif  '/school/approved_exam_record/'  in request.path:
            queryset = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(approved=True)
            total_exam_approved = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(approved=True).count()

        elif '/school/declined_exam_record/'  in request.path:
            queryset = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(declined=True)
            total_exam_declined = ExamRegistration.objects.filter(institute=request.user.id, year=year).filter(declined=True).count()
        else:
            pass

        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 30)

        try:
            exam_records = paginator.page(page)
        except PageNotAnInteger :
            exam_records = paginator.page(1)
        except EmptyPage :
            exam_records = paginator.page(paginator.num_pages)
        context = {'exam_records': exam_records, 'currentExam_total': currentExam_total, 'total_exam_submitted': total_exam_submitted
            ,'total_exam_approved': total_exam_approved, 'total_exam_declined': total_exam_declined,
            'close_query':close_query, 'year':year}

        return render(request, 'school/exam_record_list.html', context)

    elif request.user.is_authenticated and not request.user.is_school:
        return HttpResponseRedirect(reverse("Auth:Register")) 

class edit_index(UpdateView):
    model = Indexing
    form_class = IndexingForm
    template_name = 'school/add_indexing.html'
    success_url = reverse_lazy('schoolPortal:new_indexing')

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.institution = self.request.user
        form.instance.year="2021-2022"
        form.save()
        sweetify.success(self.request, 'Record updated succesffully', button='Great!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('schoolPortal:currentIndex', kwargs={"year":'2021-2022'})

class update_exam_record(UpdateView):
    model = ExamRegistration
    form_class = ExamRegForm
    template_name = 'school/Exam_reg.html'
    success_url = reverse_lazy('profPortal:dashboard') 

@login_required
def delete_record(request, id):
    if '/school/delete_record/' in request.path :
        try :
            record = Indexing.objects.get(id=id)  
        except Indexing.DoesNotExist:
            pass
        record.delete()
        sweetify.success(request, "Record has been deleted")
        return(HttpResponseRedirect(request.META['HTTP_REFERER'])) 

    elif '/school/current_exam_record/' in request.path:
        try:
            record = ExamRegistration.objects.get(id=id)
        except record.DoesNotExist:
            pass
        record.delete()
        return render(request, 'school/exam_record_list.html')

  
@login_required 
def submit_index_record(request):
    records = ''
    
    try :
        records = Indexing.objects.filter(submitted=False, institution_id=request.user.id)
        if records :
            records.update(submitted=True) 
            sweetify.success(request, 'Record has been submitted' , button='Great!')
        else:
            sweetify.error(request, 'Record Empty' , button='Ok!')

    except Indexing.DoesNotExist:
        sweetify.error(request, 'Record Doesn\'t Exist' , button='Great!')
    return(HttpResponseRedirect(request.META['HTTP_REFERER']))

@login_required
def submit_exam_record(request):
    records = ''
    try :
        print("Exam Submit Section")
        records = ExamRegistration.objects.filter(submitted=False, institute_id=request.user.id)
        print(records)
        if records :
            records.update(submitted=True) 
            sweetify.success(request, 'Record has been submitted' , button='Great!')
        else:
            sweetify.error(request, 'Record Empty' , button='Ok!')
        
    except ExamRegistration.DoesNotExist:
        sweetify.error(request, 'Record Doesn\'t Exist' , button='Great!')
    return(HttpResponseRedirect(request.META['HTTP_REFERER']))

class ViewTicket(TemplateView):
    template_name = 'school/view_ticket.html'

class CreateTicket(CreateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy("schoolPortal:all_ticket")
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
                return HttpResponseRedirect(reverse('schPortal:view_ticket', kwargs={'id':id}))
            else:
                sweetify.error(request, 'Form is not valid', button='Great!')
        else:
           sweetify.error(request, 'Ticket has been closed', button='Great!') 
    
    elif 'school/close_ticket' in request.path:
        if record.ticket_status !=  'Closed':
            record.ticket_status = 'Closed'
            record.save()
            sweetify.success(request, 'Ticket Closed', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:view_ticket', kwargs={'id':id}))
        else:
            sweetify.error(request, "Ticket Status is Closed ")
  
    return render(request, 'school/view_ticket.html', {'record': record, 'all_records': all_records})


@login_required
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
        
        elif '/school/export_current_student/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Current Student Record.xls"'

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
        
        elif '/school/export_current_student/xls/' in request.path:
            
            rows = Indexing.objects.filter(institution_id=request.user.id, submitted=False).values_list('first_name', 'middle_name', 'surname', 'cadre', 'permanent_address', 'telephone', 'email', 
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
    if '/school/export_submitted_exam_record/xls/' or '/school/export_current_exam_record/xls/' or '/school/export_approved_exam_record/xls/' in request.path: 
        request.user.id = School.objects.values_list('id', flat=True).get(User_id=request.user.id)
        response = HttpResponse(content_type='applicaton/mx-excel')
        if '/school/export_submitted_exam_record/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Submitted Record for Exam.xls"'
        elif '/school/export_current_exam_record/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Current Exam Record.xls"'
        elif '/school/export_approved_exam_record/xls/' in request.path:
            response['Content-Disposition'] = 'attachment; filename=  "Approved Exam Record.xls"'

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
        
            rows = ExamRegistration.objects.filter(institute_id=request.user.id, submitted=True).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )
    
        elif '/school/export_current_exam_record/xls/' in request.path:
            
            rows = ExamRegistration.objects.filter(institute_id=request.user.id, submitted=False).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )

        elif '/school/export_approved_exam_record/xls/' in request.path:
            
            rows = ExamRegistration.objects.filter(institute_id=request.user.id, approved=True).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )
            
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
