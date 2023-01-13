import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "localhost"
port = 1025
sender_email = "bulk@test.com"

def send_bulk_emails(email_list, subject, plain_text, html_content=None):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(plain_text, "plain")
    if html_content is not None:
        part2 = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    if html_content is not None:
        message.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server,port)
        # TODO: Send email here
        server.sendmail(sender_email, email_list, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 