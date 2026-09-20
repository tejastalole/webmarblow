import json
import logging
import os
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def notify_owner(subject, body, reply_to=None):
    """
    Send lead details to tejastalole7@gmail.com.
    Prefer Resend API, then Gmail SMTP. Browser FormSubmit is the no-config path.
    """
    recipient = getattr(settings, 'LEAD_NOTIFY_EMAIL', 'tejastalole7@gmail.com')

    resend_key = os.environ.get('RESEND_API_KEY', '').strip()
    if resend_key:
        return _send_resend(resend_key, subject, body, recipient, reply_to)

    if getattr(settings, 'EMAIL_HOST_PASSWORD', ''):
        return _send_smtp(subject, body, recipient, reply_to)

    logger.info('No RESEND_API_KEY / EMAIL_HOST_PASSWORD; relying on browser FormSubmit')
    return False


def _send_resend(api_key, subject, body, recipient, reply_to=None):
    payload = {
        'from': os.environ.get('RESEND_FROM', 'WebMarblow <onboarding@resend.dev>'),
        'to': [recipient],
        'subject': subject,
        'text': body,
    }
    if reply_to:
        payload['reply_to'] = reply_to

    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        'https://api.resend.com/emails',
        data=data,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='ignore')
        raise RuntimeError(f'Resend HTTP {exc.code}: {detail}') from exc

    logger.info('Resend mail queued for %s (%s)', recipient, result.get('id'))
    return True


def _send_smtp(subject, body, recipient, reply_to=None):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', recipient)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[recipient],
        reply_to=[reply_to] if reply_to else None,
    )
    sent = email.send(fail_silently=False)
    logger.info('SMTP mail sent to %s (%s)', recipient, sent)
    return sent


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
