import os
import smtplib


class MailClient:

    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    def send(self, receiver, subject, message):
        with smtplib.SMTP(self.server, self.port) as server:
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            message = f"Subject: {subject}\n\n{message}"
            server.sendmail(self.user, receiver, message)


def get_email_client():
    return MailClient("smtp-mail.outlook.com", 587, "felix.jobson@outlook.de", os.getenv('EMAIL_PASSWORD'))


if __name__ == "__main__":
    os.environ['EMAIL_PASSWORD'] = ""
    mail_client = get_email_client()

    receiver_email = "hauerf98@gmail.com"
    subject = "Test"
    message="""
    Dies ist ein Test 


    This message is sent from Python.
    """

    mail_client.send(receiver_email, subject, message)
