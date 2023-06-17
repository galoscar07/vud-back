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
                    <p style="color: #17616C;">Vreaudoctor.ro</p>
                </div>
            </body>
        </html>
    '''),
    'forget_password': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Reseteaza parola.</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>Primiți acest email deoarce ați solicitat că doriți schimbarea parolei contului dumneavoastră.</p>
                <p>Pentru a introduce o nouă parolă, vă rugăm să faceți click pe buton</p>
                <a href="$link" style="padding: 10px; width: 300px; background-color: #17616C; color: white;">Schimbare parolă</a>
                <p>sau să copiați linkul de acces de mai jos și să-l accesați din bara de adrese: $link</p>
                <p>Echipa,</p>
                <p style="color: #17616C;">Vreaudoctor.ro</p>
            </div>
        </body>
    </html>
    '''),
    'thankyou': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Vă mulțumim pentru înscrierea în comunitatea Vreaudoctor</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>Înainte de a putea accesa contul dumneavoastră, acesta trebuie aprobat de către administratorii Vreaudoctor.ro</p>
                <p>Vă vom trimite un email cu un link de acces după ce contul a fost aprobat.</p>
                <p>Echipa,</p>
                <p style="color: #17616C;">Vreaudoctor.ro</p>
            </div>
        </body>
    </html>
    '''),
    'account-approved': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Cont aprobat Vreaudoctor.ro</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>Suntem bucuroși să îți confirmăm aprobarea contului tău pe vreaudoctor.ro. </p>
                <p>Ai acum acces la toate funcționalitățile platformei și poți începe să îți promovezi serviciile medicale. Îți mulțumim că ai ales VreauDoctor.ro!</p>
                <a href="https://www.vreaudoctor.ro/login" style="padding: 10px; width: 300px; background-color: #17616C; color: white;">Accesează cont</a>
                <p>sau să copiați linkul de acces de mai jos și să-l accesați din bara de adrese: https://www.vreaudoctor.ro/login</p>
                <p>Echipa,</p>
                <p style="color: #17616C;">Vreaudoctor.ro</p>
            </div>
        </body>
    </html>
    '''),
    'account-denied': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Revendicare cont refuzata</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>Draga $name</p>
                <p>Iti multumim ca ai incercat sa revendici contul paginii pe vreaudoctor.ro.</p>
                <p>Din pacate, revendicarea ta nu a fost acceptata din urmatoarele motive:</p>
                <ul>
                    <li>Documentele justificative pe care le-ai furnizat nu au putut fi acceptate, deoarece nu indeplineau toate cerintele noastre.</li>
                    <li>Informatiile furnizate nu au putut fi verificate suficient pentru a demonstra ca esti reprezentantul legal.</li>
                </ul>
                <p>Iti recomandam sa verifici informatiile furnizate si sa te asiguri ca documentele justificative sunt complete si conforme cu cerintele noastre. Dupa aceea, poti sa incerci sa revendici contul din nou.</p>
                <p>In cazul in care ai intrebari suplimentare, te rugam sa ne contactezi prin email la adresa support@vreauundoctor.ro </p>
                <p>Cu respect,</p>
                <p style="color: #17616C;">Echipa VreauDoctor.ro</p>
            </div>
        </body>
    </html>
    '''),
    'invite-part-of-team': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Ai primit invitație pe Vreaudoctor.ro</h1>
            </div>
            <div style="margin-top: 30px;">
                <p>$nume te-a adăugat $typeAdded pe pagina de profil a $type de pe vreaudoctor.ro.</p>
                <p>$toSent creează-ți și tu cont, alătură-te comunității vreaudoctor.ro și ajută pacineții să te găsească mai ușor.</p>
                <a href="https://www.vreaudoctor.ro/register" style="padding: 10px; width: 300px; background-color: #17616C; color: white;">Creează cont</a>
                <p>Echipa,</p>
                <p style="color: #17616C;">Vreaudoctor.ro</p>
            </div>
        </body>
    </html>
    '''),
    'invite-part-of-team-custom': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Ai primit invitație pe Vreaudoctor.ro</h1>
            </div>
            <div style="margin-top: 30px;">
               <p>$message</p>
            </div>
        </body>
    </html>
    '''),
    'notification-invited-collab-doctor-to-clinic': Template('''
    <html>
        <body>
            <div style="margin-top: 40px; width: 100%; height: 200px; background-color: #1BB583; display: flex; flex-direction: row; justify-content: center; align-items: center; color: white;">
                <img src='cid:myimageid' width="160" height="160" >
                <h1 style="color: #FFFFFF">Ai primit invitație pe Vreaudoctor.ro</h1>
            </div>
            <div style="margin-top: 30px;">
               <p>Buna ziua, $to_name</p>
               <p>$from_name te-a adaugat colaborator pe pagina de profil de pe vreaudoctor.ro</p>
               <p>Pentru a vedea pagina de profil poti da click aici: <a href="$profile_link">$link</a></p>
            </div>
        </body>
    </html>
    '''),
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
        # Verify email to activate account
        if email_type == 'verify-email':
            template_processed = EMAIL_TEMPLATES['register'].substitute(link=data['url'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Contul dumneavoastră a fost creat.",
                "template": template_processed,
            }
            send_email(message=message)

        # Reset password token
        if email_type == 'reset-password':
            template_processed = EMAIL_TEMPLATES['forget_password'].substitute(link=data['url'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Reseteaza parola pentru contul tau de Vreaudoctor",
                "template": template_processed,
            }
            send_email(message=message)

        # Thank you for sign up email
        if email_type == 'thank-you-sign-up':
            template_processed = EMAIL_TEMPLATES['thankyou'].substitute()
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Vă mulțumim pentru înscrierea în comunitatea Vreaudoctor",
                "template": template_processed,
            }
            send_email(message=message)

        # Your account have been approved
        if email_type == 'account-approved':
            template_processed = EMAIL_TEMPLATES['account-approved'].substitute()
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Cont aprobat Vreaudoctor.ro",
                "template": template_processed,
            }
            send_email(message=message)

        # Your account have been denied
        if email_type == 'account-denied':
            template_processed = EMAIL_TEMPLATES['account-denied'].substitute(name=data['name'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Revendicarea contului pe vreaudoctor.ro",
                "template": template_processed,
            }
            send_email(message=message)

        # You received an invitation to be a part of the team
        if email_type == 'invite-part-of-team':
            if data['custom']:
                template_processed = EMAIL_TEMPLATES['invite-part-of-team-custom'].substitute(message=data['message'])
            else:
                template_processed = EMAIL_TEMPLATES['invite-part-of-team'].substitute(nume=data['name'], typeAdded=data['typeAdded'], type=data['type'], toSent=data['toSent'])
            message = {
                "from_email": SENDER,
                "from_name": "Vreau Doctor",
                "to_email": data['email'],
                "subject": "Vă mulțumim pentru înscrierea în comunitatea Vreaudoctor",
                "template": template_processed,
            }
            send_email(message=message)

