# management/commands/sendtestemail.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email to verify email settings'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipients',
            nargs='*',
            type=str,
            help='List of email recipients',
        )

    def handle(self, *args, **options):
        subject = 'Test Email'
        message = 'This is a test email to verify email settings.'
        from_email = settings.EMAIL_HOST_USER
        recipients = options['recipients'] or [settings.EMAIL_HOST_USER]

        try:
            send_mail(subject, message, from_email, recipients)
            self.stdout.write(self.style.SUCCESS(f'Test email sent successfully to {recipients}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending test email: {e}'))
