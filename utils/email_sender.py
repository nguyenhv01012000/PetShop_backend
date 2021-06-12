import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config.settings.base import (
    EMAIL_SERVER,
    EMAIL_PORT,
    EMAIL_SENDER,
    EMAIL_SENDER_NAME,
    EMAIL_PASSWORD
)

logger = logging.getLogger(__name__)


def send(to: list, subject: str, msg: str):
    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as email_server:
        email_server.starttls(context=ssl.create_default_context())
        email_server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{EMAIL_SENDER_NAME} <{EMAIL_SENDER}>"
        message["To"] = ", ".join(to)
        message.attach(MIMEText(msg, "html"))
        email_server.sendmail(EMAIL_SENDER, to, message.as_string())
        logger.debug("email sent.")