from mechanize import Browser, ParseResponse, urlopen, urljoin
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, String, Password
from pyface.api import FileDialog, warning, information, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, HistoryEditor

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.message import Message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
from email import Charset
import getpass, imaplib

def generate_email(sender, receiver, subject, body):

    # Create message container
    frame = MIMEMultipart(u'related')
    # Charset.Charset( 'utf-8' )
    # Create message container - the correct MIME type is multipart/alternative.
    # frame['Bcc'] = 'kelidas@seznam.cz'
    frame['From'] = sender
    frame['To'] = receiver
    frame['Subject'] = subject

    msg = MIMEMultipart(u'alternative')
    # Create the body of the message (a plain-text).
    text = unicode(body)

    # Record the MIME types of both parts - text/plain
    part1 = MIMEText(text, 'plain', _charset='iso-8859-2')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    frame.attach(msg)

    return frame


def send_email_smtp(sender, receiver, email, password):
    # Send the message via local SMTP server.
    s = smtplib.SMTP('ex07.fce.vutbr.cz', 587)
    # s.set_debuglevel( 1 )
    s.starttls()
    print s.login('sadilek.v@fce.vutbr.cz', password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, email.as_string())
    print s.quit()


class SMS_Email_Sender(HasTraits):

    receiver = Str
    sender = Str

    message = String(maxlen=123)

    password = Password()  # minlen=8, maxlen=8)

    send = Button('send')
    def _send_fired(self):
        email = generate_email(self.sender,
                               self.receiver,
                               self.message[:30],
                               self.message[30:])
        send_email_smtp(self.sender,
                        self.receiver,
                        email,
                        self.password)

    traits_view = View(
                       Item('receiver', editor=HistoryEditor(entries=10), id='recipient'),
                       Item('sender', editor=HistoryEditor(entries=10), id='sender'),
                       Item('message', style='custom'),
                       Item('password'),
                       Item('send'),
                        title='SMS(email)_Sender',
                        id='sms_sender.SMS_Email_Sender',
                        resizable=True,
                        width=0.5,
                        height=0.3,
                        buttons=[OKButton])


if __name__ == '__main__':
    sms = SMS_Email_Sender()
    sms.configure_traits()
