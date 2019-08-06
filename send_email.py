from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count): #email and height is captured from the user input in app.py
    from_email="adetwins2005@gmail.com"
    from_password="adeyemitj1"
    to_email=email

    subject="Height data"
    message="Hey there, your height is <strong> %s</strong>. Average height of all is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people" % (height, average_height, count)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['from']=from_email

    #to login to your gmail account
    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg) #send message
