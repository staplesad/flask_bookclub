from flask_mail import Message
from bookclub_app import mail
from flask import render_template
from config import ADMINS

def send_email(subject, sender, recipients, text_body, html_body):
    msg=Message(subject, sender=sender, recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    mail.send(msg)

def new_book_notification(book, recipients):
    send_email('New book!', ADMINS[0], recipients,
    render_template("new_book_email.txt", book=book),
    render_template("new_book_email.html",book=book))

def upcoming_notification(book, recipients):
    send_email('Upcoming book discussion', ADMINS[0], recipients,
            render_template("upcoming_email.txt", book=book),
            render_template("upcoming_email.html", book=book))
