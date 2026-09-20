import html
import logging
from email.mime.image import MIMEImage
from email.utils import formataddr
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

BRAND_BLUE = '#1a6dff'
BRAND_NAVY = '#0b1830'
BRAND_MUTED = '#5c6d82'
BRAND_PAPER = '#f4f7fb'
BRAND_LINE = '#dce5f0'
BRAND_ORANGE = '#ff8a2b'

LOGO_PATH = (
    Path(settings.BASE_DIR) / 'website' / 'static' / 'website' / 'img' / 'webmarblow-logo.png'
)
LOGO_CID = 'webmarblow-logo'


def notify_owner(subject, text_body, html_body, reply_to=None):
    """Email full lead details to tejastalole7@gmail.com via Gmail SMTP."""
    recipient = getattr(settings, 'LEAD_NOTIFY_EMAIL', 'tejastalole7@gmail.com')
    from_email = formataddr((
        'WebMarblow',
        getattr(settings, 'DEFAULT_FROM_EMAIL', recipient),
    ))

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[recipient],
        reply_to=[reply_to] if reply_to else None,
    )
    email.attach_alternative(html_body, 'text/html')
    email.mixed_subtype = 'related'

    if LOGO_PATH.exists():
        with LOGO_PATH.open('rb') as logo_file:
            logo = MIMEImage(logo_file.read(), _subtype='png')
        logo.add_header('Content-ID', f'<{LOGO_CID}>')
        logo.add_header('Content-Disposition', 'inline', filename='webmarblow-logo.png')
        email.attach(logo)

    sent = email.send(fail_silently=False)
    logger.info('Lead email sent to %s (%s)', recipient, sent)
    return sent


def _esc(value):
    return html.escape(str(value or '-'), quote=True)


def _row(label, value, link=None):
    display = _esc(value)
    if link:
        display = (
            f'<a href="{_esc(link)}" style="color:{BRAND_BLUE};'
            f'text-decoration:none;font-weight:600;">{display}</a>'
        )
    return f'''
      <tr>
        <td style="padding:12px 0;border-bottom:1px solid {BRAND_LINE};
                   width:34%;color:{BRAND_MUTED};font-size:13px;
                   font-family:Arial,Helvetica,sans-serif;vertical-align:top;">
          {_esc(label)}
        </td>
        <td style="padding:12px 0;border-bottom:1px solid {BRAND_LINE};
                   color:{BRAND_NAVY};font-size:15px;font-weight:600;
                   font-family:Arial,Helvetica,sans-serif;vertical-align:top;">
          {display}
        </td>
      </tr>
    '''


def _message_block(label, text):
    safe = _esc(text).replace('\n', '<br>')
    return f'''
      <tr>
        <td colspan="2" style="padding:20px 0 8px;color:{BRAND_MUTED};
                   font-size:13px;font-family:Arial,Helvetica,sans-serif;">
          {_esc(label)}
        </td>
      </tr>
      <tr>
        <td colspan="2" style="padding:16px 18px;background:{BRAND_PAPER};
                   border-radius:12px;color:{BRAND_NAVY};font-size:15px;
                   line-height:1.6;font-family:Arial,Helvetica,sans-serif;">
          {safe}
        </td>
      </tr>
    '''


def _wrap_html(eyebrow, title, intro, rows_html):
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
<body style="margin:0;padding:0;background:{BRAND_PAPER};">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0"
         style="background:{BRAND_PAPER};padding:28px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0"
               style="max-width:560px;background:#ffffff;border-radius:18px;
                      overflow:hidden;border:1px solid {BRAND_LINE};">
          <tr>
            <td align="left" style="padding:22px 28px 16px;background:#ffffff;
                       border-bottom:1px solid {BRAND_LINE};">
              <img src="cid:{LOGO_CID}" width="220" height="auto" alt="WebMarblow - Ideas, Websites, Growth"
                   style="display:block;border:0;outline:none;text-decoration:none;
                          max-width:220px;height:auto;">
            </td>
          </tr>
          <tr>
            <td style="background:{BRAND_BLUE};padding:22px 28px;">
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                          letter-spacing:0.14em;text-transform:uppercase;
                          color:rgba(255,255,255,0.8);margin-bottom:8px;">
                {_esc(eyebrow)}
              </div>
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:22px;
                          font-weight:700;color:#ffffff;line-height:1.3;">
                {_esc(title)}
              </div>
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;
                          color:rgba(255,255,255,0.9);margin-top:8px;">
                {_esc(intro)}
              </div>
            </td>
          </tr>
          <tr>
            <td style="padding:8px 28px 28px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                {rows_html}
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:18px 28px;background:{BRAND_PAPER};
                       border-top:1px solid {BRAND_LINE};">
              <img src="cid:{LOGO_CID}" width="140" height="auto" alt="WebMarblow"
                   style="display:block;border:0;outline:none;margin-bottom:10px;
                          max-width:140px;height:auto;">
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;
                          color:{BRAND_ORANGE};">
                Reply to this email to contact the lead directly.
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''


def format_contact_email(inquiry):
    text = (
        'New contact enquiry from WebMarblow website\n\n'
        f'Name: {inquiry.name}\n'
        f'Email: {inquiry.email}\n'
        f'Phone: {inquiry.phone or "-"}\n'
        f'Subject: {inquiry.subject}\n\n'
        'Message:\n'
        f'{inquiry.message}\n'
    )
    rows = ''.join([
        _row('Name', inquiry.name),
        _row('Email', inquiry.email, link=f'mailto:{inquiry.email}'),
        _row('Phone', inquiry.phone or '-', link=f'tel:{inquiry.phone}' if inquiry.phone else None),
        _row('Subject', inquiry.subject),
        _message_block('Message', inquiry.message),
    ])
    html_body = _wrap_html(
        eyebrow='New contact enquiry',
        title=inquiry.subject,
        intro=f'{inquiry.name} sent a message from the website.',
        rows_html=rows,
    )
    return text, html_body


def format_quote_email(quote_request):
    service = quote_request.service.title if quote_request.service else 'Not selected'
    text = (
        'New quote request from WebMarblow website\n\n'
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
    rows = ''.join([
        _row('Name', quote_request.name),
        _row('Email', quote_request.email, link=f'mailto:{quote_request.email}'),
        _row('Phone', quote_request.phone, link=f'tel:{quote_request.phone}' if quote_request.phone else None),
        _row('Company', quote_request.company or '-'),
        _row('Service', service),
        _row('Budget', quote_request.get_budget_display()),
        _row('Timeline', quote_request.get_timeline_display()),
        _message_block('Project details', quote_request.project_details),
    ])
    html_body = _wrap_html(
        eyebrow='New quote request',
        title=f'{quote_request.name} wants a quote',
        intro='Full brief from the Get a Quote form.',
        rows_html=rows,
    )
    return text, html_body
