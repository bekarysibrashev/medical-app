from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from .forms import *



class IndexView(View):
    def get(self, request):
        return render(request, 'App/main.html')
# Create your views here.

class UsView(View):
    def get(self, request):
        return render(request, 'App/us.html')

  
class MainView(View):
    def get(self, request):
        return render(request, 'App/main.html')
    
class DoctorListView(View):
    def get(self, request):
        doctors = Doctors.objects.all()
        return render(request, 'App/doctor_list.html', context={
            'doctors':doctors
        })

class ChooseTypeView(View):
    def get(self, request):
        items = Specialization.objects.all()
        print(items)
        return render(request, 'App/new.html', context={
            'items' : items
        })

    def post(self, request):    
        selected = request.POST['item']
        doctor_type = Specialization.objects.get(id=selected)
        doctors = Doctors.objects.filter(specialization=doctor_type)
        doctor_ids = ",".join([str(doctor.id) for doctor in doctors])  # Преобразуем ID врачей в строку
        url = reverse('choose_doctor') + f'?doctors={doctor_ids}'
        return redirect(url)



class ChooseDoctorView(View):
    def get(self, request):
        doctors = request.GET.get('doctors')
        print('------------')
        print('Choose Doctor GET')
        print('-------------')
        doctor_id_list = doctors.split(',')
        doctors = Doctors.objects.filter(id__in=doctor_id_list)
        return render(request, 'App/doctors.html', context={
            'doctors':doctors
        })
        
   
    def post(self, request):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        doctor_id = request.POST.get('item')
        print(doctor_id)
        return redirect(f'create_appointment/?doctor_id={doctor_id}')
        


class CreateAppointmentView(View):
    def get(self, request):
        doctor_id = request.GET.get('doctor_id')
        doctor = Doctors.objects.get(id=doctor_id)
        appointments = Appointment.objects.filter(doctor=doctor)
        request.session['doctor_id'] = doctor_id
        print(doctor)
        print('------------------------------------------------')
        form = AppointmentForm()
        return render(request, 'App/create_appointment.html', {'form': form, 'appointments': appointments})
        # return render(request, 'App/create_appointment.html')

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data.get('time')
            doctor = form.cleaned_data.get('doctor')
            request.session['time'] = time
            # print('=================================')
            # print(time)
            # print('=================================')
            return redirect('/create_patient')  
        appointments = Appointment.objects.filter(doctor=form.instance.doctor)
        return render(request, 'App/create_appointment.html', {'form': form, 'appointments': appointments})



class CreatePatientView(View):
    def get(self, request):
        form = PatientForm()
        

        return render(request, 'App/create_patient.html', context={'form': form, })

    def post(self, request):
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()

            patient_id = form.instance.id 
            patient = Patient.objects.get(id=patient_id)
            time = request.session.get('time')
            doctor_id = request.session.get('doctor_id')
            doctor = Doctors.objects.get(id=doctor_id)
            appointment_form_data = {
                'time': time,
                'patient': patient,
                'doctor': doctor
            }
            print('------------------------------')

            form_appointment = AppointmentForm(initial=appointment_form_data)
            if form_appointment.is_valid():
                form_appointment.save()
            # print(patient_id)
            # print(patient)
        
           
            # return redirect('success_page')  # Перенаправьте пользователя на страницу подтверждения
        return render(request, 'App/success.html', {'form': form})

# class CreateAppointmentView(View):
#     def get(self, request):
#         form = AppointmentForm()
#         return render(request, 'App/create_appointment.html', {'form': form})

#     def post(self, request):
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Перенаправьте пользователя на страницу подтверждения
#         return render(request, 'App/create_appointment.html', {'form': form})
    