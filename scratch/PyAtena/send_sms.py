from mechanize import Browser, ParseResponse, urlopen, urljoin
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, String, Password
from pyface.api import FileDialog, warning, information, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, HistoryEditor


class SMS_Sender(HasTraits):

    phone_number = Str

    message = String(maxlen=765)

    confirmation = Bool(True)

    password = Password(minlen=8, maxlen=8)

    send = Button('send')
    def _send_fired(self):
        br = Browser()

        # Ignore robots.txt
        br.set_handle_robots(False)
        # Google demands a user-agent that isn't a robot
        br.addheaders = [('User-agent', 'Firefox')]

        # Retrieve the Google home page, saving the response
        resp = br.open("https://www.t-mobile.cz/.gang/login-url/portal?nexturl=https%3A%2F%2Fwww.t-mobile.cz%2Fweb%2Fcz%2Fosobni")

        br.select_form(nr=2)

        br.form['username'] = 'kelidas'
        br.form['password'] = self.password

        resp = br.submit()
        #print resp.get_data()

        resp = br.open("https://sms.client.tmo.cz/closed.jsp")
        br.select_form(nr=1)

        #print br.form
        #help(br.form)

        br.form['recipients'] = self.phone_number#'736639077'#'737451193' #'605348558'
        br.form['text'] = self.message

        br.form.find_control("confirmation").get("1").selected = self.confirmation

        resp = br.submit()

        #logout
        resp = br.follow_link(url_regex='logout')

        br.close()

        information(None, 'SMS sent!')

    traits_view = View(
                       Item('phone_number', editor=HistoryEditor(entries=10), id='phone_number'),
                       Item('message', style='custom'),
                       Item('confirmation'),
                       Item('password'),
                       Item('send'),
                        title='SMS_Sender',
                        id='sms_sender.SMS_Sender',
                        dock='tab',
                        resizable=True,
                        width=0.5,
                        height=0.3,
                        buttons=[OKButton])


if __name__ == '__main__':
    sms = SMS_Sender()
    sms.configure_traits()
