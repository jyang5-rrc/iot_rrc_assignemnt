import smtplib
from email.mime.text import MIMEText


    
def send_email_alert(moisture_level, EMAIL_USERNAME, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT,EMAIL_PASSWORD):
    subject = 'Moisture Level Alert'
    message = f'Moisture level is Low: {moisture_level}'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USERNAME
    msg['To'] = RECIPIENT_EMAIL
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email sending failed:", str(e))