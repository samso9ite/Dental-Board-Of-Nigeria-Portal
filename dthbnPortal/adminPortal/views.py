from django.shortcuts import render
from django.views.generic import TemplateView
from adminPortal.models import *
from authentication.models import User, Ticket
from schPortal.models import School, Indexing
from adminPortal.views import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from adminPortal.forms import *
from django.template.defaulttags import register
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import sweetify
import xlwt
# Create your views here.

class Dashboard(TemplateView):
    template_name = 'adminPortal/dashboard.html'


def dashboard(request):
    all_school = User.objects.filter(is_school=True)[:10]
    total_sch_num = User.objects.all().count()
    total_submited_index = Indexing.objects.filter(submitted=True).count() 
    
    return render(request, 'adminPortal/dashboard.html', {'all_school':all_school, 'total_sch_num':total_sch_num, 'total_submited_index':total_submited_index})

class AccreditedSchools(TemplateView):
    template_name = 'adminPortal/indexing.html'

def school_index(request):
    records = IndexLimit.objects.filter(used_limit__gte=0)
    page = request.GET.get('page', 1)
    paginator = Paginator(records, 1)
    try:
        school_index_records = paginator.page(page)
    except PageNotAnInteger:
        school_index_records = paginator.page(1)
    except EmptyPage:
        school_index_records = paginator.page(paginator.num_pages)

    return render (request, 'adminPortal/indexing.html', {'school_index_records': school_index_records})

def accredited_schools(request):
    school_records = User.objects.filter(is_school=True).select_related('user')
   
    page = request.GET.get('page', 1)
    paginator = Paginator(school_records, 3)

    try:
        accredited_schools_record = paginator.page(page)
    except PageNotAnInteger:
        accredited_schools_record = paginator.page(1)
    except EmptyPage:
        accredited_schools_record = paginator.page(paginator.num_pages)

    return render (request, 'adminPortal/accredited.html', {'accredited_schools_record':accredited_schools_record})


@login_required
def restriction(request, id):
    
    try:
    
        user_instance = User.objects.get(id=id)
        if '/admin/block_user' in request.path :
            user_instance.block = True
            user_instance.save()
            sweetify.success(request, 'School Blocked Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))

        elif '/admin/unblock_user' in request.path :
            user_instance.block = False
            user_instance.save()
            sweetify.success(request, 'School Unblocked Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))

        elif '/admin/suspend_user' in request.path:
            user_instance.suspend = True
            user_instance.save()
            sweetify.success(request, 'School Suspended Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))

        elif '/admin/unsuspend_user' in request.path :
            user_instance.suspend = False
            user_instance.save()
            sweetify.success(request, 'School Unsuspended Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))

        elif '/admin/delete_user' in request.path :
            user_instance.delete()
            sweetify.success(request, 'School Deleted Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))

      
    except User.DoesNotExist:
        sweetify.error(request, 'School Blocked Successfully', button='Great!')
        return HttpResponseRedirect(reverse('adminPortal:accredited_schools'))



@login_required
def indexed_list(request):
    all_schools = []
    approved_index = []
    declined_index = []
    indexed = School.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(indexed, 1)
    for index_record in indexed:
        school_indexed = Indexing.objects.filter(institution=index_record.User, submitted=True).count()
        approved_index_count = Indexing.objects.filter(institution=index_record.User, approved=True).count()
        declined_index_count = Indexing.objects.filter(institution=index_record.User, unapproved=True).count()
        all_schools.append({index_record.id:school_indexed})
        approved_index.append({index_record.id:approved_index_count})
        declined_index.append({index_record.id:declined_index_count})
     
    try:
        indexed_stu_list = paginator.page(page)
    except PageNotAnInteger:
        indexed_stu_list = paginator.page(1)
    except EmptyPage:
        indexed_stu_list = paginator.page(paginator.num_pages)

    context = {'indexed_stu_list': indexed_stu_list, 'all_schools':all_schools, 
                'approved_index': approved_index, 'declined_index': declined_index}
    return render(request, 'adminPortal/indexing.html', context)


@register.filter
def get_item(all_schools, key):
    for all_sch in all_schools:
        if key in all_sch:
            return all_sch.get(key)

@register.filter
def get_item( approved_index, key):
    for all_approved in  approved_index:
        if key in all_approved:
            return all_approved.get(key)

@register.filter
def get_item(declined_index, key):
    for all_declined in declined_index:
        if key in all_declined:
            return all_declined.get(key)
    

@login_required
def reset_limit(request, id):
    sch_data = School.objects.get(id=id)
    form = setLimit(request.POST or None, instance = sch_data) 
    if form.is_valid():
        form.save()
    sweetify.success(request, 'Updated Successfully', button='Great!')
    return HttpResponseRedirect(reverse('adminPortal:indexed_list'))

@login_required
def reverse_submission(request, id):
    try:
        if 'admin/reverse_index_record' in request.path:
            school_instance = Indexing.objects.filter(institution_id=id, submitted=True)
            none_sch_instances = Indexing.objects.filter(institution_id=id, submitted=False)
        elif 'admin/reverse_exam_record/' in request.path:
            print(id)
            school_instance = ExamRegistration.objects.filter(institute_id=id, submitted=True)
            none_sch_instances = ExamRegistration.objects.filter(institute_id=id, submitted=False)
        if school_instance:
            school_instance.update(submitted=False, approved=False, declined=False)
            sweetify.success(request, 'Reversed Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:indexed_list'))

        elif none_sch_instances:
            sweetify.error(request, 'Record Hasn\'t been submitted', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:indexed_list'))
       
    except Indexing.DoesNotExist:
        sweetify.error(request, 'Record Not Found', button='Great!')
        return HttpResponseRedirect(reverse('adminPortal:indexed_list'))


@login_required
def sch_indexed_rec(request, id):
    sch_id = id
    record = ''
    if 'admin/sch_indexed_rec/' in request.path:
        record = Indexing.objects.filter(institution_id=id, submitted=True)

    elif 'admin/approve_index/' in request.path:
        record = Indexing.objects.get(id=id, submitted=True)
        record.approved = True
        record.unapproved = False
        record.comment = ''
        record.save()
        sweetify.success(request, 'Approved Successfully', button='Great!')
        return HttpResponseRedirect(reverse('adminPortal:dashboard'))
    
    elif 'admin/decline_index/' in request.path:
        record = Indexing.objects.get(id=id, submitted=True)
        form = UpdateIndexStatus(request.POST, instance=record)
        if form.is_valid():
            form.save()
            sweetify.error(request, 'Declined Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:dashboard'))
    elif 'admin/approved_indexed_list/' in request.path:
        record = Indexing.objects.filter(institution_id=id, approved=True)
    elif 'admin/declined_indexed_list/' in request.path:
        record = Indexing.objects.filter(institution_id=id, unapproved=True)
    else:
        pass
    sch_name = User.objects.values_list('username', flat=True).get(id=id)
  
    page = request.GET.get('page', 1)
    paginator = Paginator(record, 2)

    try:
        all_sch_records = paginator.page(page)
    except PageNotAnInteger:
        all_sch_records = paginator.page(1)
    except EmptyPage:
        all_sch_records = paginator.page(paginator.num_pages)
    return render(request, 'adminPortal/school_indexed_record.html', {'all_sch_records': all_sch_records, 'sch_name':sch_name, 'sch_id': sch_id})

class Exam(TemplateView):
    template_name = 'adminPortal/Examination_dept.html'
    

def exam_record(request):
    all_records = []
    approved_records = []
    declined_records = []

    all_schools = School.objects.all()

    for each_school in all_schools:
        total_exam_record = ExamRegistration.objects.filter(institute=each_school.id, submitted=True).count()
        approved_exam_record = ExamRegistration.objects.filter(institute=each_school.id, approved=True).count()
        declined_exam_record = ExamRegistration.objects.filter(institute=each_school.id, declined=True).count()
        all_records.append({each_school.id:total_exam_record})
        approved_records.append({each_school.id:approved_exam_record})
        declined_records.append({each_school.id:declined_exam_record})
    
    page = request.GET.get('page', 1)
    paginator = Paginator(all_schools, 1)

    try:
        all_school_record = paginator.page(page)
    except PageNotAnInteger:
        all_school_record = paginator.page(1)
    except EmptyPage:
        all_school_record = paginator(paginator.num_pages)
    context =  {'all_school_record':all_school_record, 'all_records': all_records,'approved_records': approved_records, 'declined_records': declined_records}
    return render(request, 'adminPortal/Examination_dept.html', context)

@register.filter
def get_item(all_records, key):
    for record in all_records:
        if key in record:
            return record.get(key)

@register.filter
def get_item(approved_records, key):
    for record in approved_records:
        if key in record:
            return record.get(key)

@register.filter
def get_item(declined_records, key):
    for record in declined_records:
        if key in record:
            return record.get(key)

@login_required
def exam_rec(request, id):
  
    sch_id = id
    if 'admin/sch_exam_rec/' in request.path:
        record = ExamRegistration.objects.filter(institute_id=id, submitted=True)

    elif 'admin/approve_student/' in request.path:
        print(id)
        record = ExamRegistration.objects.get(id=id, submitted=True)
        record.approved = True
        record.declined = False
        record.comment = ''
        record.save()
        sweetify.success(request, 'Approved Successfully', button='Great!')
        return HttpResponseRedirect(reverse('adminPortal:dashboard'))
    
    elif 'admin/decline_student/' in request.path:
        record = ExamRegistration.objects.get(id=id, submitted=True)
        form = UpdateExamStatus(request.POST, instance=record)
        if form.is_valid():
            form.save()
            sweetify.error(request, 'Declined Successfully', button='Great!')
            return HttpResponseRedirect(reverse('adminPortal:dashboard'))

    elif 'admin/approved_exam_rec/' in request.path:
        record = ExamRegistration.objects.filter(institute_id=id, approved=True)

    elif 'admin/declined_exam_rec/' in request.path:
        record = ExamRegistration.objects.filter(institute_id=id, declined=True)

    sch_name = School.objects.get(id=id)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(record, 1)

    try:
        all_exam_records = paginator.page(page)
    except PageNotAnInteger:
        all_exam_records = paginator.page(1)
    except EmptyPage:
        all_exam_records = paginator.page(paginator.num_pages)
    return render(request, 'adminPortal/sch_exam_record.html', {'all_exam_records': all_exam_records, 'sch_name':sch_name, 'sch_id': sch_id})


@login_required
def reset_exam_limit(request, id):
    sch_data = School.objects.get(id=id)
    form = setExamLimit(request.POST or None, instance = sch_data) 
    if form.is_valid():
        form.save()
        sweetify.success(request, 'Updated Successfully', button='Great!')
    return HttpResponseRedirect(reverse('adminPortal:exam_record'))


@login_required
def ticket_list(request):
    if request.user.is_authenticated and request.user.is_admin:
        schools = []
        if 'admin/all_ticket' in request.path:
            all_schools = User.objects.filter(is_school=True)
            all_schools_count = Ticket.objects.filter(first_created=True).count()
            for sch in all_schools:
                sch_replies = Ticket.objects.filter(user_id=sch.id, ticket_status='School Reply', read=False).count()
                open_ticket = Ticket.objects.filter(user_id=sch.id, ticket_status='Open', read=False).count()
                closed_ticket = Ticket.objects.filter(user_id=sch.id, ticket_status='Closed').count()
                answered_ticket = Ticket.objects.filter(user_id=sch.id, ticket_status='Answered').count()
              
                if sch_replies or open_ticket or answered_ticket:
                    schools.append({'sch_replies':sch_replies, 'sch_details': sch, 'open_ticket': open_ticket, 
                    'closed_ticket': closed_ticket, 'answered_ticket': answered_ticket})
                  
            context = {'sch_replies': sch_replies, 'schools': schools,  'closed_ticket': closed_ticket, 'answered_ticket':answered_ticket,
                        'open_ticket': open_ticket}
                
            return render(request, 'adminPortal/ticket_list.html', context)
    else:
        return HttpResponseRedirect(reverse("Auth:Register")) 
        
@login_required
def sch_ticket_list(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        if 'admin/sch_reply_list/' in request.path:
            query = Ticket.objects.filter(user_id = id, ticket_status='School Reply', read=False)
        elif 'admin/answered_ticket_list' in request.path:
            query = Ticket.objects.filter(user_id=id, ticket_status='Answered')
        elif 'admin/opened_ticket_list' in request.path:
            query = Ticket.objects.filter(user_id= id, ticket_status='Open', read=False)
        elif 'admin/closed_ticket_list' in request.path:
            query = Ticket.objects.filter(user_id=  id, ticket_status='Closed')
        # print(query)

        page = request.GET.get('page', 1)
        paginator = Paginator(query, 3)

        try:
            query_list = paginator.page(page)
        except PageNotAnInteger:
            query_list = paginator.page(1)
        except EmptyPage:
            query_list = paginator.page(paginator.num_pages)

        return render(request, 'adminPortal/sch_ticket_list.html', {'query_list':query_list})

    
    

@login_required
def export_school(request):
    response = HttpResponse(content_type='applicaton/mx-excel')
    response['Content-Disposition'] = 'attachment; filename="Accredited Schools.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Schools')

    # Sheet Header, First Row  
    row_num = 0
   
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['School Name', 'Registration Number', 'Programme', 'School Address', 'Phone Number', 'Email', 
                    'State', 'Postal Address', 'HOD\'s Name', 'HOD\'s Number', 'HOD\'s Email',]
        
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet Body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.filter(is_school=True).values_list('username', 'code', 'programme', 'user__address', 'phone_number', 'email', 'user__region', 
    'user__postal_number', 'user__hod_name', 'user__hod_phone', 'user__hod_email')
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
  

    wb.save(response)
    return response



def export_indexed_stu(request, id):
   

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Schools')

    # Sheet Header, First Row
    row_num = 0
   
    font_style = xlwt.XFStyle()
    font_style.font.bold = True   
    if '/admin/export_indexed_student/xls/' in request.path: 
        sch_name = User.objects.values_list('username', flat=True).get(id=id)  
        response = HttpResponse(content_type='applicaton/mx-excel')
        response['Content-Disposition'] = 'attachment; filename=  "{} Indexing Record.xls"'.format(sch_name)
        columns = ['First Name', 'Middle Name',  'Surname',  'Cadre', 'Permanent Address', 'Phone Number', 'Email', 
                        'Age', 'State Of Origin', 'Religion', 'Nationality', 'Marital Status', 'School Attended(1)', 'Qualification(1)', 'School Attended(2)', 'Qualification(2)',
                        'School Attended(3)', 'Qualification(3)', 'School Attended(4)', 'Qualification(4)', 'Year of Admission', 
                        'Year of Graduation', 'Contact Address', 'Place of Work', 'Referee Name(1)', 'Referee Address(1)', 'Referee Mobile(1)'
                        'Referee Name(2)', 'Referee Address(2)', 'Referee Mobile(2)',]
            
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet Body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Indexing.objects.filter(institution_id=id, submitted=True).values_list('first_name', 'middle_name', 'surname', 'cadre', 'permanent_address', 'telephone', 'email', 
        'age', 'state', 'religion', 'nationality', 'marital_status', 'school_attended1', 'qualification1', 'school_attended2', 'qualification2',
            'school_attended3', 'qualification3', 'admission_year', 'graduation_year', 'contact_address', 'place_of_work', 
            'referee_name1', 'referee_address1', 'referee_phone1', 'referee_name2', 'referee_address2', 'referee_phone2')

    elif '/admin/export_exam_record/' in request.path:
        sch_id = School.objects.values_list('User_id', flat=True).get(id=id)
        sch_name = User.objects.values_list('username', flat=True).get(id=sch_id)


        response = HttpResponse(content_type='applicaton/mx-excel')
        response['Content-Disposition'] = 'attachment; filename=  "{} Exam Record.xls"'.format(sch_name)
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
        # sch_id = School.objects.get(id=id)
        sch_id = School.objects.values_list('id', flat=True).get(id=id)
        print(sch_id)
        rows = ExamRegistration.objects.filter(institute_id=sch_id, submitted=True).values_list('title', 'first_name', 'middle_name', 'surname', 'cadre', 'residential_address', 'telephone', 'email', 
                 'date_of_birth', 'state_of_origin', 'religion', 'marital_status', 'maiden_name', 'senatorial_district', 'qualification1', 'qualification2', 'qualification3', 'qualification4', 'prof_qualification1',
                  'prof_qualification2', 'prof_qualification3', 'prof_qualification4', 'institution_attended1', 'institution_attended2', 'institution_attended3', 'institution_attended4', 'hod_name', 'hod_phone', 'hod_email',
                  'employment_status', 'office_name', 'office_address', 'office_country', 'office_lga', 'office_phone', 'office_email', 'sector', 'present_position', 'department' )
    
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
