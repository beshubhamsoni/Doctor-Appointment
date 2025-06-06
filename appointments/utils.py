from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

def send_appointment_email(appointment):
    """Send email notification to doctor about new appointment"""
    subject = 'New Appointment Request'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = appointment.doctor.user.email

    # Context for email template
    context = {
        'doctor_name': appointment.doctor.user.get_full_name(),
        'patient_name': appointment.patient.user.get_full_name(),
        'patient_phone': appointment.patient.phone_number,
        'appointment_date': appointment.date,
        'appointment_time': appointment.time,
        'reason': appointment.reason,
        'login_url': f"{settings.SITE_URL}{reverse('login')}"
    }

    # Render HTML content
    html_content = render_to_string('appointments/email/new_appointment.html', context)
    text_content = strip_tags(html_content)  # Plain text version of email

    # Create email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email]
    )
    
    # Attach HTML content
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False 