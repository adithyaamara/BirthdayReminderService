from logging import exception
import os
import smtplib, ssl

class EmailClient:
    def __init__(self) -> None:
        # Read Required Environment variables.
        try:
            # The github action workflow reads git secrets at run time and exports them as env variables to make them available to program. 
            self.__sender_email_id = os.getenv('SENDER_EMAIL_ID')
            self.__sender_email_passwd = os.getenv('SENDER_EMAIL_PASSWORD')
            # > Note : Less secure apps are no more supported by gmail. Use an app password instead of actual mail password.
            self.__subscribers = str(os.getenv('NOTIFICATION_SUBSCRIBERS')).split(',')
            self.__port = 587  # For SSL
        except Exception as err:
            print()
            exit(err)

        # Initiate hand shake.
        try:
            # Create a secure SSL context
            context = ssl.create_default_context()
            self.__server = smtplib.SMTP("smtp.gmail.com",self.__port)
            self.__server.ehlo()
            self.__server.starttls(context=context) # Secure the connection
            self.__server.ehlo()
        except Exception as err:
            print(err)
            exit("Unexpected Error During HandShake with gmail server!!!")

        # Login to server
        try:
            self.__server.login(self.__sender_email_id, self.__sender_email_passwd)
        except smtplib.SMTPAuthenticationError as err:
            print(err)
            exit("Invalid Username / Password, Authentication Rejected by server.")
        except Exception as err:
            print(err)
            exit("Unable to login to smtp server for unknown reasons!!")
        print("Successfully Authenticated with E-Mail Server.")

    def SendMail_Wrapper(self, Subject: str, Message: str, Receivers = None):
        """
        Wrapper function for building and sending email messages.\n
        If None is given for receivers, it will default to subscribers read from env.\n
        Otherwise a list of email ids can be supplied to specify receivers. 
        """
        if Receivers is None:
            Receivers = self.__subscribers
        Message_Body = 'Subject: {}\n\n{}'.format(Subject, Message)  # form message with subject and body.
        try:
            self.__server.sendmail(self.__sender_email_id, Receivers, Message_Body)
        except Exception as err:
            print(format(err))
            print("Unexpected error while sending email!!")

    def release_connection_wrapper(self):
        """
        This method has to be called at the end of script.\n
        This releases the current server's SMTP handshake, active connection after which no emails can be sent.
        """
        try:
            self.__server.quit()
        except exception as err:
            print(err)
            exit("Error While Closing SMTP Connection!!")
            