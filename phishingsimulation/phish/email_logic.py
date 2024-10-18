from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def send_simulation_emails(request, user_email, username):
    # Get the current site domain
    current_site = get_current_site(request)
    domain = current_site.domain
    
    # Email subjects
    email_subject_real = "Important: Confirm Your Credentials"
    email_subject_fake = "Security Alert: Please Update Your Account"
    
    # Real email content
    real_link_context = {
        'username': username,
        'real_link': f'http://{domain}/real/',  # Real link URL
    }
    real_message_html = render_to_string('real_email.html', real_link_context)
    real_message_plain = strip_tags(real_message_html)

    # Fake phishing email content
    fake_link_context = {
        'username': username,
        'fake_link': f'http://{domain}/fake/',  # Fake phishing link URL
    }
    fake_message_html = render_to_string('fake_email.html', fake_link_context)
    fake_message_plain = strip_tags(fake_message_html)

    # Send the real email
    send_mail(
        email_subject_real,
        real_message_plain,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=real_message_html,
    )
    
    # Send the phishing (fake) email
    send_mail(
        email_subject_fake,
        fake_message_plain,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=fake_message_html,
    )

    return "Simulation emails sent."
