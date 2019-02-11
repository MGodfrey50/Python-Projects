import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# This function attaches and picture and emails.
# Required parameters are email_user (sender), email_rec (recipient), subject and filename
# the filename includes the path

# These parameters will be passed by the main program when it's assembled
email_user = 'alarm-alert@outlook.com'
email_rec = 'cdn.mgodfrey@gmail.com'
msg_body = 'Hi There, sending email from Python'
filename ='c:\Coding\Send eMail\IMG_1673.JPG'
subject = 'Generated by RPi Camera'

def Send_eMail(email_filename, email_to ,email_from, email_subject):
    msg=MIMEMultipart()
    msg['To']=email_to
    msg['From'] =email_from
    msg['Subject'] = email_subject

    attachment = open(email_filename, 'rb')
    part = MIMEBase ('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename ="+filename)

    msg.attach(part)
    msg.attach(MIMEText(msg_body,'plain'))
    text=msg.as_string()

    server = smtplib.SMTP('smtp.live.com',587)
    server.starttls()
    server.login(email_from, "1million!")

    server.sendmail(email_from, email_to,text)
    server.quit()



Send_eMail(filename, email_rec,email_user,subject)
