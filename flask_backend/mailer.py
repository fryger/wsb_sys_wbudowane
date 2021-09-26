import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tinydb import TinyDB, Query

db = TinyDB('./db.json')

table = db.table('Email')
config = table.all()[0]
sender = config['sender']
password = config['pass']
receiver = config['receiver']

def send_email(name, spots):
    with open('output.jpg', 'rb') as f:
        img_data = f.read()

    mail_content = f"Cześć, na parkingku {name} jest {spots} wolnych miejsc!"
    sender_address = sender
    sender_pass = password
    receiver_address = receiver
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'Parking {name} , wolne miejsca {spots}'   
    
    message.attach(MIMEText(mail_content, 'plain'))
    image = MIMEImage(img_data, name='parking.jpg')
    message.attach(image)
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

if __name__ == "__main__":
    send_email('Reda przód', '6')
