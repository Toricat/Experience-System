import smtplib
import emails 
from app.core.config import settings


class EmailData:
    html_content: str
    subject: str



def send_email(
        *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
    attachments: list[str] = [],
    ) -> None:

    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    if attachments:
        message.attach()

    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response =   message.send(to=email_to, smtp=smtp_options)
    print(response)
   
    









# def send_email(
#     *,
#     email_to: str,
#     subject: str = "",
#     html_content: str = "",
# ) -> None:
#     assert settings.emails_enabled, "no provided configuration for email variables"
#     message = emails.Message(
#         subject=subject,
#         html=html_content,
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     elif settings.SMTP_SSL:
#         smtp_options["ssl"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, smtp=smtp_options)
#     logging.info(f"send email result: {response}")