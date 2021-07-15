
import datetime
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

fromaddr = "facerecreport@gmail.com" #enter sender's email address.
toaddr = input("Enter Teacher's Email address in \" \" :" ) #enter receiver's (TEACHER's) email address.

# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = fromaddr 

# storing the receivers email address 
msg['To'] = toaddr 

# storing the subject 
yz = datetime.datetime.now()
yzl = yz.strftime("%x")
msg['Subject'] = "Attendance Report for date :"+yzl

# string to store the body of the mail 
body = "Classroom attendance Report from face recognition based attendance."

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
filename = "attendance.csv"
attachment = open(r"E:\face\GUICode\innovators.csv", "rb") #Enter the address of the CSV containing attendance report according to your PC libraries & folders.

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
p.set_payload((attachment).read()) 

# encode into base64 
encoders.encode_base64(p) 

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(fromaddr, "VpNk18262933") #Enter the password of sender's email account.

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
s.sendmail(fromaddr, toaddr, text) 

# terminating the session 
s.quit() 
