import emails 
from core.config import settings
from pathlib import Path

def render_email_template(template_name: str, **kwargs) -> str:
    """
    Renders an HTML email template with provided key-value pairs.

    :param template_name: The name of the HTML template file (e.g., 'register_code.html').
    :param kwargs: Key-value pairs to replace in the template.
    :return: A string containing the rendered HTML.
    """
    project_root = Path(__file__).resolve().parent.parent.parent.parent

    template_path = (project_root / "app" / "email-templates" / "build" / template_name)
    print(template_path)
    # template_path = "c:\\Users\\hamin\\Documents\\GitHub\\Personal\\1_Authentication\\server\\app\\email-templates\\build\\register_code.html"
    # template_path = "c:/Users/hamin/Documents/GitHub/Personal/1_Authentication/server/app/email-templates/build/register_code.html"
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
        print(template_content)

    for key, value in kwargs.items():
        placeholder = f"{{{{ {key} }}}}"
        template_content = template_content.replace(placeholder, value)

    return template_content

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

    response = message.send(to=email_to, smtp=smtp_options)
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