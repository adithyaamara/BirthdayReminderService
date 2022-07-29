import pandas as pd
from datetime import datetime as dt
from email_client import EmailClient
import time

mail_client = EmailClient()     # Initialize email mechanism.
subject = "[Notification] - Event Reminder service"  # The Subject line for this service mails.

# Read the csv file having events and fill undeclared values with None
events = pd.read_csv('Events.csv').fillna("None")

# Drop rows where DATE field is None
events = events[events.DATE != "None"].reset_index()

# Parse Dates and separate dat, month columns
events['day'] = events['DATE'].str.split('-', expand=True)[0].astype('int')
events['month'] = events['DATE'].str.split('-', expand=True)[1].astype('int')

# filter events
current_day = dt.now().day
current_month = dt.now().month
events = events[events['month'] == current_month].sort_values(ascending=True, by='day')  # Focus on Current Month
events_today = events[events['day'] == current_day]         # Filter by today's date.
events_tomorrow = events[events['day'] == current_day+1]    # Tomorrows events.

# filter future events in current month, except tomorrow
events_this_month = events[events['day'] > current_day+1]

# Message for Today events
if len(events_today) == 0:
    message = "There are no Events Today!!!\n"
else:
    message = ''
    for i in range(len(events_today)):
        message = message + f"{events_today.iloc[i].NAME} is celebrating his / her {events_today.iloc[i].EVENT_NAME} today!!!!\n"
        # Send personalized email if person's email id is available
        if events_today.iloc[i].EMAIL != "None":
            personal_message = f"I wish you many more happy returns of the day, all good and success on occasion of your {events_today.iloc[i].EVENT_NAME}. \n -- Adithya Amara"
            personal_subject = "Greetings to you!!!!"
            mail_client.SendMail_Wrapper(Subject=personal_subject, Message=personal_message, Receivers=str(events_today.iloc[i].EMAIL))
            time.sleep(2)   # Add little delay.

# Message for tomorrow events
if(len(events_tomorrow)) != 0:
    for i in range(len(events_tomorrow)):
        message = message + f"\n{events_tomorrow.iloc[i].NAME} is celebrating his / her {events_tomorrow.iloc[i].EVENT_NAME} tomorrow.\n"

# Message for upcoming events in this month
if len(events_this_month) == 0:
    message = message + '\nThere are no more events in this month :('
else:
    for i in range(len(events_this_month)):
        message = message + f"\n{events_this_month.iloc[i].NAME} is going to celebrate his / her {events_this_month.iloc[i].EVENT_NAME} on {events_this_month.iloc[i].day} of this month!!!!\n"
print(message)

# Send Email
mail_client.SendMail_Wrapper(Subject=subject, Message=message)
# Release SMTP Connection
mail_client.release_connection_wrapper()
