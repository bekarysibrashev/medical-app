from django.urls import path 
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('choose_type', ChooseTypeView.as_view(), name='choose_type'),
    path('choose_doctor', ChooseDoctorView.as_view(), name='choose_doctor'),
    path('create_appointment/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('create_patient/', CreatePatientView.as_view(), name='create_patient'),
    path('main/', MainView.as_view(), name='main'),  
    path('doctor_list/', DoctorListView.as_view(), name='doctor_list'),  
    path('us/', UsView.as_view(), name='us'),  

]