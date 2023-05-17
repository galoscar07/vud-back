import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from django.template.loader import render_to_string

# SENDER = 'vudpentrumine@gmail.com'
SENDER = 'vudpentrumine@gmail.com'
SENDER_PASSWORD = 'lsytmnyjrivwzgkk'

EMAIL_TEMPLATES = {
    'register':  Template('''
        <html>
            <body>
                <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                    <img src='cid:myimageid' width="160" height="160" >
                    <h1 style="color: #FFFFFF">Contul dumneavoastră a fost activat.</h1>
                </div>
                <div style="margin-top: 30px;">
                    <p>Vă rugăm să vă logați cu datele dumneavoastră de cont.</p>
                    <p>Pentru a accesa contul dumneavoastră, vă rugăm să faceți click pe buton</p>
                    <a href="$link" style="padding: 10px; width: 300px; background-color: #17616C; color: white;"> ACCES CONT</a>
                    <p>sau să copiați linkul de acces de mai jos și să-l accesați din bara de adrese: $link</p>
                    <p>Echipa,</p>
                    <p style="color: #17616C;">Vreauundoctor.ro</p>
                </div>
            </body>
        </html>
    '''),
    'forget_password': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Cont înregistrat cu succes.</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>Primiți acest email deoarce ați solicitat că doriți schimbarea parolei contului dumneavoastră.</p>
                <p>Pentru a introduce o nouă parolă, vă rugăm să faceți click pe buton</p>
                <a href="$link" style="padding: 10px; width: 300px; background-color: #17616C; color: white;">Schimbare parolă</a>
                <p>sau să copiați linkul de acces de mai jos și să-l accesați din bara de adrese: $link</p>
                <p>Echipa,</p>
                <p style="color: #17616C;">Vreauundoctor.ro</p>
            </div>
        </body>
    </html>
''')
}


def attach_file_to_email(email_message, filename, extra_headers=None):
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    email_message.attach(file_attachment)


def send_email(message):
    email_message = MIMEMultipart()
    email_message['From'] = message['from_email']
    email_message['To'] = message['to_email']
    email_message['Subject'] = message['subject']

    attach_file_to_email(email_message, 'authentication/Logo.png', {'Content-ID': '<myimageid>'})

    email_message.attach(MIMEText(message['template'], "html"))

    email_string = email_message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, SENDER_PASSWORD)
        server.sendmail(message['from_email'], message['to_email'], email_string)


class Util:
    @staticmethod
    def send_email(data, email_type):
        if email_type == 'verify-email':
            template_processed = EMAIL_TEMPLATES['register'].substitute(link=data['url'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Verificati email-ul pentru a finaliza crearea de cont",
                "template": template_processed,
            }
            send_email(message=message)

        if email_type == 'reset-password':
            template_processed = EMAIL_TEMPLATES['forget_password'].substitute(link=data['url'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Reseteaza parola pentru contul tau de Vreau Un Doctor",
                "template": template_processed,
            }
            send_email(message=message)
