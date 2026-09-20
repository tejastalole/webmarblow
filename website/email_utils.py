from django.conf import settings
from django.core.mail import EmailMessage


def notify_owner(subject, body, reply_to=None):
    """Send lead/quote details to the business inbox."""
    recipient = getattr(settings, 'LEAD_NOTIFY_EMAIL', 'tejastalole7@gmail.com')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', recipient)

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[recipient],
        reply_to=[reply_to] if reply_to else None,
    )
    return email.send(fail_silently=False)


def format_quote_email(quote_request):
    service = quote_request.service.title if quote_request.service else 'Not selected'
    return (
        'New quote request from WebMarblow website\n'
        '========================================\n\n'
        f'Name: {quote_request.name}\n'
        f'Email: {quote_request.email}\n'
        f'Phone: {quote_request.phone}\n'
        f'Company: {quote_request.company or "-"}\n'
        f'Service: {service}\n'
        f'Budget: {quote_request.get_budget_display()}\n'
        f'Timeline: {quote_request.get_timeline_display()}\n\n'
        'Project details:\n'
        f'{quote_request.project_details}\n'
    )


def format_contact_email(inquiry):
    return (
        'New contact enquiry from WebMarblow website\n'
        '==========================================\n\n'
        f'Name: {inquiry.name}\n'
        f'Email: {inquiry.email}\n'
        f'Phone: {inquiry.phone or "-"}\n'
        f'Subject: {inquiry.subject}\n\n'
        'Message:\n'
        f'{inquiry.message}\n'
    )
