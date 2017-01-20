import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emailer:
    def __init__(self):
        pass

    def send_mail(self, destination, message, subject = "Test subject"):
        fromaddr = "text.missing.info"
        toaddr = destination
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Email Test Subject"

        body = message
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "parolaparola")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
