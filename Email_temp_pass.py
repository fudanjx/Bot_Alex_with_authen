import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendemail(temp_password, user_email):

    # Email configuration
    sender_email = "bot_Alex@outlook.com"
    receiver_email = user_email
    subject = "Your temporary password"
    message = "Your temporay password is" + temp_password

    # SMTP server configuration
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "bot_Alex@outlook.com"
    smtp_password = 'DedricTammy123!@#'

    # Create the email message
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject
    email.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server
    smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
    smtp_obj.starttls()  # Enable TLS encryption
    smtp_obj.login(smtp_username, smtp_password)

    # Send the email
    smtp_obj.sendmail(sender_email, receiver_email, email.as_string())

    # Disconnect from the SMTP server
    smtp_obj.quit()

    print("Email sent successfully!")