from django.template.loader import render_to_string
from django.core.signing import Signer
from api.settings import ALLOWED_HOSTS
from django.core.mail import send_mail

signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    send_mail(subject, body_text, None, [user.email])