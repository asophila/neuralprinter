#!/usr/bin/env python
# encoding: utf-8
"""
https://gist.github.com/rdempsey/22afd43f8d777b78ef22
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.
This script works with Python 3.x
NOTE: replace values in ALL CAPS with your own values
"""

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '
sender = ''
password = ''
smtp = ''


def email(recipients, attachments, body):
    
    if not(sender and password and smtp):
        print("Configurar cuenta de correo")
        return

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Practia te pinta'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = ''
    outer.attach(MIMEText(body, 'html'))
    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("No se pudo abrir los adjuntos.")
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP(smtp, 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Correo enviado.")
    except:
        print("No se pudo enviar el correo.")
        raise
