from django.core.mail import send_mail
from django.template.loader import render_to_string

from vudback import settings


class Util:
    @staticmethod
    def send_email(data, email_type):
        if email_type == 'verify-email':
            msg_plain = render_to_string('verify_email.txt', data)
            msg_html = render_to_string('verify_email.html', data)
            # send_mail(
            #     subject='Verificati email-ul pentru a finaliza crearea de cont',
            #     message=msg_plain,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[data['email'], ],
            #     html_message=msg_html
            # )
        if email_type == 'reset-password':
            msg_plain = render_to_string('verify_email.txt', data)
            msg_html = render_to_string('verify_email.html', data)
            # send_mail(
            #     subject='Verificati email-ul pentru a finaliza resetarea parolei',
            #     message=msg_plain,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[data['email'], ],
            #     html_message=msg_html
            # )

