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
        notify_owner(
            subject='WebMarblow test email',
            body=(
                'This is a test email from WebMarblow.\n'
                'If you received this, SMTP is configured correctly.\n'
            ),
            reply_to=settings.EMAIL_HOST_USER,
        )
        self.stdout.write(self.style.SUCCESS(f'Test email sent to {recipient}'))
