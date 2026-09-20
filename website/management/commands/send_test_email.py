from django.conf import settings
from django.core.management.base import BaseCommand

from website.email_utils import notify_owner


class Command(BaseCommand):
    help = 'Send a test email to LEAD_NOTIFY_EMAIL using current SMTP settings.'

    def handle(self, *args, **options):
        if not settings.EMAIL_HOST_PASSWORD:
            self.stderr.write(
                self.style.ERROR(
                    'EMAIL_HOST_PASSWORD is empty. Set a Gmail App Password first.'
                )
            )
            return

        recipient = settings.LEAD_NOTIFY_EMAIL
        text = (
            'This is a test email from WebMarblow.\n'
            'If you received this, SMTP is configured correctly.\n'
        )
        html_body = (
            '<div style="font-family:Arial,Helvetica,sans-serif;padding:24px;">'
            '<h2 style="color:#0b1830;">WebMarblow test email</h2>'
            '<p style="color:#5c6d82;">SMTP is configured correctly.</p>'
            '</div>'
        )
        notify_owner(
            subject='WebMarblow test email',
            text_body=text,
            html_body=html_body,
            reply_to=settings.EMAIL_HOST_USER,
        )
        self.stdout.write(self.style.SUCCESS(f'Test email sent to {recipient}'))
