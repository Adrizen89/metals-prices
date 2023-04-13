import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    # Informations de connexion SMTP de Microsoft
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    username = 'adrienberard@hotmail.fr'
    password = '!Sbteam0109*'

    # Informations sur l'e-mail
    sender = 'adrienberard@hotmail.fr'
    receiver = 'adri.brrd@outlook.fr'
    subject = 'Objet de votre e-mail'
    body = 'Contenu de votre e-mail'

    # Création de l'e-mail
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP de Microsoft
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)

    # Envoi de l'e-mail
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
