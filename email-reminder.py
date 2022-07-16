import pandas as pd
from datetime import datetime as dt
from email_client import EmailClient

mail_client = EmailClient()     # Initialize email mechanism.
subject = "[Notification] - Event Reminder service"  # The Subject line for this service mails.

# Read the csv file having events and fill undeclared values with None
events = pd.read_csv('Events.csv').fillna("None")

# Drop rows where DATE field is None
events = events[events.DATE != "None"].reset_index()

# filter events happening today
current_day = '{:02d}'.format(dt.now().day)       # Current day in 2 digit string format.
current_month = '{:02d}'.format(dt.now().month)   # Current month in 2 digit string format.
events = events[events.DATE == f"{current_day}-{current_month}"]    # Filter by today's date.

if len(events) == 0:
    message = "There are no Events Today!!!"
else:
    message = ''
    for i in range(len(events)):
        message = message + f"{events.iloc[i].NAME} is celebrating his / her {events.iloc[i].EVENT_NAME} today!!!!\n"
print(message)

# Send Email
mail_client.SendMail_Wrapper(Subject=subject, Message=message)
# Release SMTP Connection
mail_client.release_connection_wrapper()
