from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'schoolPortal'
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    # path('update/(?P<pk>\d+)/edit/', views.AccountUpdate.as_view(), name="update"),
    path('<User>/update', views.AccountUpdate, name="update"),
    path('schoolprofile/', views.SchoolProfile.as_view(), name='schoolProfile'),
    path('ajax/load-lga/', views.load_cities, name='ajax_load_region'),
    path('new_indexing/', views.NewIndexingView.as_view(), name='new_indexing'),
    path('exam_reg/', views.ExamReg.as_view(), name="exam_reg"),
    path('indexed_record/', views.IndexListView, name='indexed_record'),
    path('current_index', views.IndexListView, name='currentIndex'),
    path('approved_student/', views.IndexListView, name='approved_student'),
    path('unapproved_student/', views.IndexListView, name='unapproved_student'),
    path('current_exam_record/', views.ExamListView, name='current_exam_record'),
    path('submitted_exam_record/', views.ExamListView, name='submitted_exam_record'),
    path('approved_exam_record/', views.ExamListView, name='approved_exam_record'),
    path('declined_exam_record/', views.ExamListView, name='declined_exam_record'),
    path('<int:id>/update_indexing', views.edit_index, name='update_indexing'),
    path('<int:id>/update_exam_record', views.update_exam_record, name='update_exam_record'),
    path('delete_record/<int:id>', views.delete_record, name='delete_record'),
    path('submit_all_index', views.submit_index_record, name='submit_all_index'),
    path('submit_all_exam_record', views.submit_exam_record, name='submit_all_exam_record'),
    
    # Ticket Urls
    # path('ticket', views.Ticket.as_view(), name='ticket'),  
    path('view_ticket', views.ViewTicket.as_view(), name='ticket'), 
    path('create_ticket', views.CreateTicket.as_view(), name='create_ticket'),
    path('all_ticket', views.ticket_list, name='all_ticket'),
    path('answered_ticket', views.ticket_list, name='answered_ticket'),
    path('closed_ticket', views.ticket_list, name='closed_ticket'),
    path('opened_ticket/', views.ticket_list, name='opened_ticket'),
    path('view_a_ticket/<int:id>', views.view_a_ticket, name='view_a_ticket'),
    path('update_ticket/<int:id>', views.view_a_ticket, name='update_ticket'),
    path('close_ticket/<int:id>', views.view_a_ticket, name='close_ticket'),
    # path('update_ticket/<int:id>', views.update_ticket, name='update_ticket'),

    path('export_indexed_student/xls/', views.export_indexed_stu, name='export_indexed_stu'),
    path('export_approved_student/xls/', views.export_indexed_stu, name='export_approved_student'),
    path('export_current_exam_record/xls/', views.export_exam_record, name='export_current_exam_record'),
    path('export_submitted_exam_record/xls/', views.export_exam_record, name='export_submitted_exam_record'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    