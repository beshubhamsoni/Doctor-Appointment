from django.contrib import admin
from .models import Patient, Doctor, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username', 'reason')
