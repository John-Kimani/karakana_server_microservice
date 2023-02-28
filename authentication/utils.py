from django.core.mail import EmailMessage
class Util:
    '''
        Method to use this class method without instanciating the class itself
    '''
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'],to=[data['to_email']])

        email.send()