from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import json

from builtins import int
from builtins import round
from builtins import super

from forex_python.converter import CurrencyRates
from future import standard_library
from mechanicalsoup.utils import LinkNotFoundError
from decimal import Decimal
from currency_converter import CurrencyConverter
import ast

from cloudomate.gateway.bitpay import BitPay
from cloudomate.hoster.vps.solusvm_hoster import SolusvmHoster
from cloudomate.hoster.vps.vps_hoster import VpsOption

standard_library.install_aliases()


class LineVast(SolusvmHoster):
    CART_URL = 'https://panel.linevast.de/cart.php?a=view'

    def __init__(self, settings):
        super(LineVast, self).__init__(settings)

    '''
    Information about the Hoster
    '''

    @staticmethod
    def get_clientarea_url():
        return 'https://panel.linevast.de/clientarea.php'

    @staticmethod
    def get_gateway():
        return BitPay

    @staticmethod
    def get_metadata():
        return 'linevast', 'https://linevast.de/'

    @staticmethod
    def get_required_settings():
        return {
            'user': ['firstname', 'lastname', 'email', 'phonenumber', 'password'],
            'address': ['address', 'city', 'state', 'zipcode'],
        }

    '''
    Action methods of the Hoster that can be called
    '''

    @classmethod
    def get_options(cls):
        """
        Linux (OpenVZ) and Windows (KVM) pages are slightly different, therefore their pages are parsed by different
        methods. Windows configurations allow a selection of Linux distributions, but not vice-versa.
        :return: possible configurations.
        """
        browser = cls._create_browser()
        browser.open("https://linevast.de/en/offers/ddos-protected-vps-hosting.html")
        options = cls._parse_openvz_hosting(browser.get_current_page())
        lst = list(options)

        return lst

    def purchase(self, wallet, option):
        self._browser.open(option.purchase_url)
        self._server_form()
        self._browser.open(self.CART_URL)

        summary = self._browser.get_current_page().find('div', class_='summary-container')
        self._browser.follow_link(summary.find('a', class_='btn-checkout'))

        form = self._browser.select_form(selector='form#frmCheckout')
        form['acceptdomainwiderruf1'] = True
        form['acceptdomainwiderruf2'] = True
        self._fill_user_form(self.get_gateway().get_name())

        self._browser.select_form(nr=0)  # Go to payment form
        self._browser.submit_selected()
        self.pay(wallet, self.get_gateway(), self._browser.get_url())

    '''
    Hoster-specific methods that are needed to perform the actions
    '''

    def _server_form(self):
        """
        Fills in the form containing server configuration.
        :return:
        """
        form = self._browser.select_form('form#frmConfigureProduct')
        self._fill_server_form()
        try:
            form['configoption[61]'] = '657'  # Ubuntu 16.04
        except LinkNotFoundError:
            form['configoption[125]'] = '549'  # Ubuntu 16.04
        self._browser.submit_selected()

    @classmethod
    def _parse_openvz_hosting(cls, page):
        urls = cls._get_hrefs()
        storage = cls._get_storage()
        names = page.find_all('p', {'class': 'text-center py-3'})
        prices = page.find_all('div', {'class': 'pricing-1'})
        info = page.find_all('div', {'class': 'text-muted'})
        for i in range(0, len(info)):
            index = 2 * i + 1
            price = str(prices).split('data-monthly="')[index].split('" data-yearly=')[0]
            name = str(names[i]).split('data-product="')[1].split('" href')[0]

            option = cls._parse_linux_option(price, name, info[i], urls[i], storage[i])
            yield option

    @staticmethod
    def _parse_linux_option(price, name, info, url, storage):
        elements = str(info).split('<br/>')
        price = price.replace(',', '.')
        c = CurrencyConverter()

        option = VpsOption(
            name=str(name).strip(),
            storage=str(storage).strip(),
            cores=str(elements[0].split('>')[1].split(' CPU-Cores')[0]).strip(),
            memory=str(elements[2].split('GB Arbeitsspeicher')[0]).strip(),
            bandwidth=str('unmetered').strip(),
            connection=str(int(elements[3].split('GB')[0]) * 1000).strip(),
            price=str(round(c.convert(price, 'EUR', 'USD'), 2)).strip(),
            purchase_url=str(url).strip(),
        )
        return option

    @classmethod
    def _get_hrefs(cls):
        browser = cls._create_browser()
        browser.open("https://panel.linevast.de/cart.php")
        page = browser.get_current_page()
        hrefs = page.find_all('a', {'class': 'order-button'})

        lst = [None] * len(hrefs)

        for x in range(0, len(hrefs)):
            urlstring = str(hrefs[x]).split('href="')[1].split('"')[0]
            urlstring = urlstring.replace('/cart.php', '').replace('amp;', '')
            url = browser.get_url()
            url = url.split('?')[0]
            url = url + urlstring
            lst[x] = url

        return lst

    @classmethod
    def _get_storage(cls):
        browser = cls._create_browser()
        browser.open("https://panel.linevast.de/cart.php")
        page = browser.get_current_page()

        storage = [None] * 4

        for x in range(0, 4):
            storagetemp = page.find('li', {'id': 'product' + str(x+1) +'-feature3'})
            storagetemp = str(storagetemp).split('>')[1].split('GB')[0]
            storage[x] = int(storagetemp)

        return storage

    @staticmethod
    def _extract_vi_from_links(links):
        for link in links:
            if "_v=" in link.url:
                return link.url.split("_v=")[1]
        return False

    @staticmethod
    def _check_login(text):
        data = json.loads(text)
        if data['success'] and data['success'] == '1':
            return True
        return False
