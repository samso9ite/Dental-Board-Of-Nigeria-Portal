from django.urls import re_path as url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'schoolPortal'
urlpatterns = [
    path('indexing/pdf/<slug:slug>', views.Pdf.as_view(), name='pdf_view'),
    path('', views.Dashboard, name='dashboard'),
    # path('update/(?P<pk>\d+)/edit/', views.AccountUpdate.as_view(), name="update"),
    path('<User>/update', views.AccountUpdate, name="update"),
    path('schoolprofile/', views.SchoolProfile.as_view(), name='schoolProfile'),
    path('ajax/load-lga/', views.load_cities, name='ajax_load_region'),
    path('new_indexing/', views.NewIndexingView.as_view(), name='new_indexing'),
    path('exam_reg/', views.ExamReg.as_view(), name="exam_reg"),
    path('exam_regis/', views.create_exam_record, name="new_exam"),
    path('indexed_record/<str:year>', views.IndexListView, name='indexed_record'),
    path('current_index/<str:year>', views.IndexListView, name='currentIndex'),
    path('approved_student/<str:year>', views.IndexListView, name='approved_student'),
    path('unaproved_student/<str:year>', views.IndexListView, name='unapproved_student'),
    path('current_exam_record/<str:year>', views.ExamListView, name='current_exam_record'),
    path('submitted_exam_record/<str:year>', views.ExamListView, name='submitted_exam_record'),
    path('approved_exam_record/<str:year>', views.ExamListView, name='approved_exam_record'),
    path('declined_exam_record/<str:year>', views.ExamListView, name='declined_exam_record'),
    path('update_indexing/<int:pk>', views.edit_index.as_view(), name='update_indexing'),
    path('update_exam_record/<int:pk>/', views.update_exam_record.as_view(), name='update_exam_record'),
    path('delete_record/<int:id>', views.delete_record, name='delete_record'),
    path('submit_all_index', views.submit_index_record, name='submit_all_index'),
    path('submit_all_exam_record', views.submit_exam_record, name='submit_all_exam_record'),

    path('ajax/load/', views.load_cities, name='ajax_load'),
    path('ajax/lga/', views.load_lga, name='ajax_lga'),
    path('ajax/load_lga/', views.load_state, name='ajax_load_lga'),
    path('ajax/load_origin/', views.load_state_origin, name='ajax_load_origin'),
    path('ajax/load_office_cities/', views.load_office_cities, name='load_office_cities'),
    path('ajax/load_office_lga/', views.load_office_lga, name='load_office_lga'),
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
    path('export_current_student/xls/', views.export_indexed_stu, name='export_current_student'),
    path('export_current_exam_record/xls/', views.export_exam_record, name='export_current_exam_record'),
    path('export_submitted_exam_record/xls/', views.export_exam_record, name='export_submitted_exam_record'),
    path('export_approved_exam_record/xls/', views.export_exam_record, name='export_approved_exam_record'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    