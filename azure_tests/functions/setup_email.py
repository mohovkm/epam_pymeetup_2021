import smtplib
from email.mime.multipart import MIMEMultipart
from os import getenv


def hotmail_provider_send_mail(receiver_email, text):
    port = getenv("HOTMAIL_PORT", 587)
    smtp_server = getenv("HOTMAIL_SMTP", "smtp.live.com")
    sender_email = getenv("HOTMAIL_SENDER")
    password = getenv("HOTMAIL_PASSWORD")

    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "A test mail sent by Python."
    message["Body"] = text

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit


PROVIDERS = {
    "hotmail": hotmail_provider_send_mail,
}


def send_email(provider: str):
    try:
        return PROVIDERS[provider]
    except KeyError as e:
        raise KeyError(f"Can't find provider name for a {provider}") from e
