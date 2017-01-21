import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer:
    @staticmethod
    def send_mail(destination, message, subject="No subject"):
        fromaddr = "text.missing.info"
        toaddr = destination
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'HTML'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "parolaparola")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
