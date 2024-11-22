from django.core.mail import send_mail


def send_deactivation_email(user):
    send_mail(
        'Your account has been deactivated',
        'Your account has been marked as inactive. If this was a mistake, please contact support.',
        'noreply@example.com',
        [user.email],
        fail_silently=False,
    )
