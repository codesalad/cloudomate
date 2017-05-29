import sys

from bs4 import BeautifulSoup

import cloudomate.gateway.bitpay
from cloudomate.vps.hoster import Hoster
from cloudomate.vps.vpsoption import VpsOption


class CrownCloud(Hoster):
    name = "crowncloud"
    website = "http://crowncloud.net/"
    required_settings = [
        'firstname',
        'lastname',
        'email',
        'address',
        'city',
        'state',
        'zipcode',
        'phonenumber',
        'password',
        'rootpw'
    ]
    clientarea_url = 'https://crowncloud.net/clients/clientarea.php'
    client_data_url = 'https://crowncloud.net/clients/modules/servers/solusvmpro/get_client_data.php'

    def __init__(self):
        super(CrownCloud, self).__init__()

    def register(self, user_settings, vps_option):
        """
        Register CrownCloud provider, pay through BitPay
        :param user_settings: 
        :param vps_option: 
        :return: 
        """
        self.br.open("https://crowncloud.net")
        self.br.open(vps_option.purchase_url)
        self.br.select_form(nr=2)
        self.fill_in_server_form()
        self.br.submit()
        self.br.open('https://crowncloud.net/clients/cart.php?a=view')
        self.br.select_form(nr=2)
        self.fill_in_user_form(user_settings)
        promobutton = self.br.form.find_control(type="submitbutton", nr=0)
        promobutton.disabled = True
        page = self.br.submit()
        if "checkout" in page.geturl():
            soup = BeautifulSoup(page.get_data(), 'lxml')
            errors = soup.findAll('div', {'class': 'errorbox'})
            print(errors[0].text)
            sys.exit(1)
        self.br.select_form(nr=0)
        page = self.br.submit()
        amount, address = cloudomate.gateway.bitpay.extract_info(page.geturl())
        return amount, address

    def fill_in_server_form(self):
        """
        Fills in the form containing server configuration.
        :return: 
        """
        self.br.form['configoption[1]'] = ['56']
        self.br.form['configoption[8]'] = ['52']
        self.br.form['configoption[9]'] = '0'
        self.br.form.new_control('text', 'ajax', {'name': 'ajax', 'value': 1})
        self.br.form.new_control('text', 'a', {'name': 'a', 'value': 'confproduct'})
        self.br.form.method = "POST"

    def fill_in_user_form(self, user_settings):
        """
        Fills in the form with user information.
        :param user_settings: settings
        :return: 
        """
        self.br.form['firstname'] = user_settings.get("firstname")
        self.br.form['lastname'] = user_settings.get("lastname")
        self.br.form['email'] = user_settings.get("email")
        self.br.form['phonenumber'] = user_settings.get("phonenumber")
        self.br.form['companyname'] = user_settings.get("companyname")
        self.br.form['address1'] = user_settings.get("address")
        self.br.form['city'] = user_settings.get("city")
        countrycode = user_settings.get("countrycode")

        # State input changes based on country: USA (default) -> Select, Other -> Text
        self.br.form['state'] = user_settings.get("state")
        self.br.form['postcode'] = user_settings.get("zipcode")
        self.br.form['country'] = [countrycode]
        self.br.form['password'] = user_settings.get("password")
        self.br.form['password2'] = user_settings.get("password")
        self.br.form['paymentmethod'] = ['bitpay']
        self.br.find_control('accepttos').items[0].selected = True

    def start(self):
        clown_page = self.br.open('http://crowncloud.net/openvz.php')
        return self.parse_options(clown_page)

    def parse_options(self, page):
        soup = BeautifulSoup(page, 'lxml')
        tables = soup.findAll('table')
        for details in tables:
            for column in details.findAll('tr'):
                if len(column.findAll('td')) > 0:
                    yield self.parse_clown_options(column)

    @staticmethod
    def beautiful_bandwidth(bandwidth):
        if bandwidth == '512 GB':
            return '0.5'
        else:
            return bandwidth.split('T')[0]

    @staticmethod
    def parse_clown_options(column):
        elements = column.findAll('td')
        option = VpsOption()
        option.name = elements[0].text
        ram = elements[1].text.split('/')[0]
        ram = float(ram.split('M')[0]) / 1024
        option.ram = str(ram)
        option.storage = elements[2].text.split('G')[0]
        option.cpu = elements[3].text.split('v')[0]
        option.bandwidth = CrownCloud().beautiful_bandwidth(elements[4].text)
        connection = int(elements[7].text.split('G')[0]) * 1000
        option.connection = str(connection)
        option.price = elements[8].text
        option.price = option.price.split('$')[1]
        option.price = option.price.split('/')[0]
        option.purchase_url = elements[9].find('a')['href']
        return option

    def get_status(self, user_settings):
        self._clientarea_get_status(user_settings, self.clientarea_url)

    def set_rootpw(self, user_settings):
        self._clientarea_set_rootpw(user_settings, self.clientarea_url)

    def get_ip(self, user_settings):
        self._clientarea_get_ip(user_settings, self.clientarea_url, self.client_data_url)