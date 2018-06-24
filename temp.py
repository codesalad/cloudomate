import os
from cloudomate.util.settings import Settings
from cloudomate.hoster.vps.blueangelhost import *
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
from fake_useragent import UserAgent
import time
import re
import requests

config = Settings()

config.read_settings('/media/xubuntu/usbdata/blueangelhost15-6config.cfg')

user_agent = UserAgent(fallback="Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0")
browser = StatefulBrowser(user_agent=user_agent.random)

ca_url = 'https://www.billing.blueangelhost.com/clientarea.php'
email_url = 'https://www.billing.blueangelhost.com/viewemail.php'

ca = BAHClientArea(browser, ca_url, email_url, config)

print ca.get_server_information_from_email()
