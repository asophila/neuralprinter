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

COMMASPACE = ', '
sender = ''
password = ''
smtp = 'smtp.office365.com'


def email(recipients, attachments):
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Practia te pinta'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

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
            print("Unable to open one of the attachments.")
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
        print("Email sent!")
    except:
        print("Unable to send the email.")
        raise
