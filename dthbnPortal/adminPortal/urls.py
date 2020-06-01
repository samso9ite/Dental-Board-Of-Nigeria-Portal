from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'adminPortal'
urlpatterns = [
    path('hboard', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('indexing', views.AccreditedSchools.as_view(), name='indexing'),
    path('school_indexed_record', views.school_index, name='school_indexed_record'),
    path('accredited_schools', views.accredited_schools, name='accredited_schools'),
    path('block_user/<int:id>', views.restriction, name='block_user'),
    path('unblock_user/<int:id>', views.restriction, name='unblock_user'),
    path('suspend_user/<int:id>', views.restriction, name='suspend_user'),
    path('unsuspend_user/<int:id>', views.restriction, name='unsuspend_user'),
    path('delete_user/<int:id>', views.restriction, name='delete_user'),
    path('indexed_list', views.indexed_list, name='indexed_list'),
    # path('sch_indexed_list/<int:id>', views.indexed_list, name='sch_indexed_list'),
    path('sch_indexed_rec/<id>', views.sch_indexed_rec, name='sch_indexed_rec'),
    path('approved_indexed_list/<int:id>', views.sch_indexed_rec, name='approved_indexed_list'),
    path('declined_indexed_list/<int:id>', views.sch_indexed_rec, name='declined_indexed_list'),
    path('approve_index/<int:id>', views.sch_indexed_rec, name='approve_index'),
    path('decline_index/<int:id>', views.sch_indexed_rec, name='decline_index'),
    path('set_limit/<int:id>', views.reset_limit, name='set_limit'),
    path('exam', views.Exam.as_view()),
    path('exam_record', views.exam_record, name='exam_record'),
    path('sch_exam_rec/<int:id>', views.exam_rec, name='sch_exam_rec'),
    path('approved_exam_rec/<int:id>', views.exam_rec, name='approved_exam_rec'),
    path('declined_exam_rec/<int:id>', views.exam_rec, name='declined_exam_rec'),
    path('approve_student/<int:id>', views.exam_rec, name='approve_student'),
    path('decline_student/<int:id>', views.exam_rec, name='decline_student'),
    path('exam_limit/<int:id>', views.reset_exam_limit, name='exam_limit'),
    path('reverse_index_record/<int:id>', views.reverse_submission, name='reverse_index_record'),
    path('reverse_exam_record/<int:id>', views.reverse_submission, name='reverse_exam_record'),

    # Ticket Urls
    path('all_ticket', views.ticket_list, name='all_ticket'),
    path('answered_ticket', views.ticket_list, name='answered_ticket'),
    path('closed_ticket', views.ticket_list, name='closed_ticket'),
    path('opened_ticket/', views.ticket_list, name='opened_ticket'),

    # Admin Tickets
    path('sch_reply_list/<int:id>', views.sch_ticket_list, name='sch_reply_list'),
    path('answered_ticket_list/<int:id>', views.sch_ticket_list, name='answered_ticket_list'),
    path('closed_ticket_list/<int:id>', views.sch_ticket_list, name='closed_ticket_list'),
    path('opened_ticket_list/<int:id>', views.sch_ticket_list, name='opened_ticket_list'),
    path('update_ticket/<int:id>', views.view_a_ticket, name='update_ticket'),
    path('view_ticket/<int:id>', views.view_a_ticket, name='view_ticket'),
    path('close_ticket/<int:id>', views.view_a_ticket, name='close_ticket'),
    path('reset_notification', views.dashboard, name='reset_notification'),

    #Professional Records
    path('professionals/', views.professionals, name='professionals'),

    path('export/xls/', views.export_school, name='export_school_xls'),
    path('export_indexed_student/xls/<int:id>', views.export_indexed_stu, name='export_indexed_student'),
    path('export_exam_record/xls/<int:id>', views.export_indexed_stu, name='export_exam_record'),
    
]
