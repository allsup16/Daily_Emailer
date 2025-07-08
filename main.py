import smtplib
import os
import helper
from email.message import EmailMessage
from dotenv import load_dotenv    
    
load_dotenv()

password = os.getenv('App_Password')

file = "config"



def main():

    creds = helper.auth()
    todays_tasks = helper.tasks(creds)


    #Email
    instructions = helper.LoadInstructions("config")
    sender = instructions['Sender']
    reciever = instructions['Reciever']
    subject = instructions['Subject']
    message = ''
    if instructions['Message']['Program_Retrieval_List']['Date']==True:
        message += 'Today: '+helper.today()
    if instructions['Message']['Text']!=None:
        message += instructions['Message']['Text']
    message+='\n\nTasks:'
    for x in todays_tasks:
            message+='\n'+x
    print(message)

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()
    server.login(sender,password)
    #server.sendmail(sender,reciever,text) 

main()