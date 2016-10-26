from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

#I dont think you need \\ just use \ if on a MAC. Although \\ might work. Try that first. 

file = "/Desktop/EHHOP/emailer/email.png" ### USER! This is where your image goes
rootdir = "/Desktop/EHHOP/emailer/" ### USER!The root directory where you keep filename
filename = "physiciancontactinfo.csv" # USER! This is your CSV, the file with the physicians names you will work from. 
me = "insert.name@icahn.mssm.edu" #USER! Put your ICAHN username
gmail_user = me
gmail_pwd = '' ## USER! put your password between quotes

def get_emails(rootdir, filename):
    email_list = []
    with open(rootdir + filename, "rU") as file:
        g = file.readlines()
        for eachline in g:
            email_list.append(eachline.split(",")[2])
    return email_list

def get_names(rootdir, filename):
    name_list = []
    with open(rootdir + filename, "rU") as file:
        g = file.readlines()
        for eachline in g:
            name_list.append(eachline.split(",")[1])
    return name_list

def get_exceptions(rootdir, filename):
    exceptions = []
    with open(rootdir + filename, "rU") as file:
        g = file.readlines()
        for eachline in g:
            exceptions.append(eachline.split(",")[7])
    return exceptions


def send_email(recipient, recipientnamestring): ##BRI! Test by writing send_email('my_email@addres.com', 'The_last_name_of_the_Dr')
    msg = MIMEMultipart()
    msg['Subject'] = "Fall precepting at EHHOP" ## BRI! Place your subject here! Again, between quotes
    msg['From'] = me
    msg['To'] = recipient

    # BRI! Create the body of the message (This is HTML). BRI! Use <br> as the enter button. Place hyperlinks between the quotes. 
    html = ''
    with open("email.html","r") as fp:
    	html = fp.read()
    html = html %(recipientnamestring)

    #Embed an image here. You only need to know if "file" is calling the image you want to. Handle that above. 
    fp = open(file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()

    # Record the MIME types of both parts - text/plain and text/html.
    body = MIMEText(html, 'html')
    msg.attach(body)
    msg.attach(img)

    ##Handling servers
    server = smtplib.SMTP("smtp.gmail.com", 587) 
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(me, recipient, msg.as_string())
    server.close()

def loop_email(): #BRI! This is what you will write when you want to send the emails. You will type loop_email() into the python shell (2.7.9).
    names = get_names(rootdir, filename)
    emails = get_emails(rootdir, filename)
    exceptions = get_exceptions(rootdir, filename)
    for i in range(1,len(emails)):
        if exceptions[i].strip('\n') != '1':
            send_email(emails[i], names[i])
        else:
            print("%s was skipped because they were on your exceptions list" % (names[i]))

if __name__ == "__main__":
    loop_email()
