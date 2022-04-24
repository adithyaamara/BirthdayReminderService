import pandas as pd
import datetime
import os
import smtplib, ssl

# Read Required Environment variables
sender_email_id = os.getenv('SENDER_EMAIL_ID')
sender_email_passwd = os.getenv('SENDER_EMAIL_PASSWORD')
# > Note : Less secure apps are no more supported by gmail. Use an app password instead of actual mail password.
subscribers = os.getenv('NOTIFICATION_SUBSCRIBERS')
port = 587  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()
server = smtplib.SMTP("smtp.gmail.com",port)
server.ehlo()
server.starttls(context=context) # Secure the connection
server.ehlo()

# Login to server
server.login(sender_email_id, sender_email_passwd)
subject = "[Notification] - Event Reminder service"  # The Subject line for this service mails.
# Read the csv file having events and fill undeclared values with None
events = pd.read_csv('Events.csv',).fillna("None")

todays_events = []  # Holds indices of above data frame where event is today.

for i in range(len(events)):
    row = events.iloc[i]
    if row.DATE != "None" and int(datetime.datetime.now().month) == int(str(row.DATE)[str(row.DATE).index('-')+1:]) and int(datetime.datetime.now().day) == int(str(row.DATE)[:str(row.DATE).index('-')]):
        print(row)
        todays_events.append(i)

if len(todays_events) == 0:
    message = "There are no Events Today!!!"
else:
    message = ''
    for i in range(len(todays_events)):
        message = message + f"{events.iloc[todays_events[i]].NAME} is celebrating his / her {events.iloc[todays_events[i]].EVENT_NAME} today!!!!\n"
print(message)
message = 'Subject: {}\n\n{}'.format(subject, message)  # form message with subject and body.
server.sendmail(sender_email_id, subscribers, message)
server.quit()