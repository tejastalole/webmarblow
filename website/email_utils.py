import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def notify_owner(subject, body, reply_to=None):
    """
    Send lead/quote details to tejastalole7@gmail.com.
    Uses Gmail SMTP when EMAIL_HOST_PASSWORD is set; otherwise FormSubmit.
    """
    recipient = getattr(settings, 'LEAD_NOTIFY_EMAIL', 'tejastalole7@gmail.com')

    if getattr(settings, 'EMAIL_HOST_PASSWORD', ''):
        try:
            return _send_smtp(subject, body, recipient, reply_to)
        except Exception:
            logger.exception('SMTP email failed; trying FormSubmit fallback')

    try:
        return _send_formsubmit(subject, body, recipient, reply_to)
    except Exception:
        logger.exception('FormSubmit email failed for %s', recipient)
        raise


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


def _send_formsubmit(subject, body, recipient, reply_to=None):
    payload = {
        'name': 'WebMarblow Website',
        'email': reply_to or recipient,
        '_subject': subject,
        '_template': 'table',
        'message': body,
    }
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'https://formsubmit.co/ajax/{recipient}',
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'WebMarblow/1.0',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='ignore')
        raise RuntimeError(f'FormSubmit HTTP {exc.code}: {detail}') from exc

    if str(result.get('success', '')).lower() not in {'true', '1'}:
        raise RuntimeError(f'FormSubmit rejected mail: {result}')

    logger.info('FormSubmit mail queued for %s', recipient)
    return True


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
