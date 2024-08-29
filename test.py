
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
def send_email(
        *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
    attachments: list[str] = [],
    ) -> bool:

    
    
    # Create the MIME message
    message = MIMEMultipart()
    message['From'] = formataddr(("Test", "test@localhost"))
    message['To'] = email_to
    message['Subject'] = subject
    
    # Attach the HTML content
    message.attach(MIMEText(html_content, 'html'))
    print("here")
    # Attach any files
    for attachment in attachments:
        part = MIMEBase('application', "octet-stream")
        try:
            with open(attachment, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment}"')
            message.attach(part)
        except Exception as e:
            print(f"Failed to attach file {attachment}: {e}")
            return False

    # Connect to the SMTP server and send the email
    try:
        print("here0")
        # server = smtplib.SMTP("smt.gmail.com", 587, timeout=120)
        # # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # print("here10")
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        print("here10")
        # with smtplib.SMTP("smtp.gmail.com", 587) as server:
        #     server.ehlo()
        #     server.starttls()
        #     server.ehlo()
        #     server.login( "meongaoda2002@gmail.com","snoy olle tdwg qhgt")
        #     server.sendmail("meongaoda2002@gmail.com", email_to, message.as_string())
        #     server.quit()
        server = smtplib.SMTP("smtp.gmail.com", 587) 

        server.starttls()

        server.login( "meongaoda2002@gmail.com","snoy olle tdwg qhgt")
        server.sendmail("meongaoda2002@gmail.com", email_to, message.as_string())
        server.quit()
        print("here1",server)
        # server.login( "meongaoda2002@gmail.com","meongaoda18122002")


        print(f"Email sent successfully to {email_to}")
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {email_to}: {e}")
        return False
send_email( email_to="haminhquan12c7@gmail.com" )