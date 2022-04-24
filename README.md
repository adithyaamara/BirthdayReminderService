# BirthDay Reminder Service
Reminds me of Birthdays, events via email to one or more persons. [As declared in `Events.csv`]

# Setup
1. Just fork 🍴 this repo.
2. Edit `Events.csv` to add as many events as you wish and save it. Update whenever needed too. (**Don't change column structure or names, otherwise code changes are needed.**)
3. Add the following `repository level secrets` to your forked repository. [Python scripts need these to send email, workflow `main.yml` supplies the same as env variables to python script]

   - `SENDER_EMAIL_ID` --> The email_id from which you want to send the reminder emails from. (Probably one of your own) 
   - `SENDER_EMAIL_PASSWORD` --> The login password for the above email_id. [Generated App password for gmail]
     
     > Using just the email password Works for most email providers.
     > **In case of G-Mail**, you either have to 
     > 1. Enable 'Less secure apps' in your gmail account to be able to send emails using python [Less secure, Temporary, Not Recommended]
     > OR
     > 2. Enable 2 Factor authentication in your google account, **Generate an app password for gmail, use the same as password and paste it as secret for `SENDER_EMAIL_PASSWORD`** (App password must included spaces too!!). [Secure, Recommended]

   - `NOTIFICATION_SUBSCRIBERS` --> The email_id or array of email_ids who wants to receive these reminder emails.

**That's It!! Now you will never forget a special day 🍰!!**

# Important:
  - I recommend that, who ever fork this repo, **Please keep the forked repo as `Priavate Repository`**. 
  - Because `Events.csv` is going to hold names, birthdays, dates of special events which are classified as `personally identifiable information`, **Keeping this in public repository attracts a potential risk of data mis-use by scamsters.**

# Credits : 
 - Thanks to **@github** for providing free runner minutes to all public repositories too, which made something like this possible ;)
