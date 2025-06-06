from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, DoctorRegistrationForm, AppointmentForm
from .models import Patient, Doctor, Appointment
from django.contrib.auth.models import User, Group
from .utils import send_appointment_email

def register_patient(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            patient = Patient.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'appointments/register.html', {'form': form, 'user_type': 'Patient'})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            doctor = Doctor.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                specialization=form.cleaned_data['specialization']
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'appointments/register.html', {'form': form, 'user_type': 'Doctor'})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient = Patient.objects.get(user=request.user)
            appointment.patient = patient
            appointment.save()

            # Send email notification to doctor
            if send_appointment_email(appointment):
                messages.success(request, 'Appointment booked successfully! The doctor has been notified.')
            else:
                messages.success(request, 'Appointment booked successfully! However, there was an issue notifying the doctor.')
            
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
def my_appointments(request):
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
        context = {'appointments': appointments, 'user_type': 'Patient'}
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        context = {'appointments': appointments, 'user_type': 'Doctor'}
    else:
        appointments = []
        context = {'appointments': appointments, 'user_type': 'Unknown'}
    
    return render(request, 'appointments/my_appointments.html', context)

@login_required
def update_appointment_status(request, appointment_id):
    if hasattr(request.user, 'doctor'):
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user.doctor)
        status = request.POST.get('status')
        if status in ['CONFIRMED', 'CANCELLED']:
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment {status.lower()} successfully!')
    return redirect('my_appointments')
