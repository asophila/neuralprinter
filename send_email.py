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
sender = 'practiatepinta@practia.global'
password = 'Practia1632'
smtp = 'owa.pragmaconsultores.net'


def email(recipients, attachments):
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Practia te pinta'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = ''
    outer.attach(MIMEText('Gracias por asistir al stand de Practia en el evento América Digital 2017.\n\nTe enviamos la imagen que fue procesada usando Redes Neuronales.\n\nHay miles de proyectos digitales esperando ser abordados, Practia ya está listo para ayudarte a concretarlos.\n'))
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

email(['gsalazar@practia.global'], ['images/practia.jpg'])
