from cloudomate.cmdline import *
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
from fake_useragent import UserAgent
import time
import re
import requests

if __name__ == "__main__":

    user_agent = UserAgent(fallback="Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0")
    browser = StatefulBrowser(user_agent=user_agent.random)

    browser.open('https://vm.linevast.de')
    browser.select_form('form')
    browser['username'] = 'vmuser8146'
    browser['password'] = 'xdt84Ic3axuQ'
    browser.submit_selected()

    browser.open('https://vm.linevast.de')
    soup = browser.get_current_page()
    pattern = re.compile(r'control\.php\?_v=(.+)')
    ahref = soup.findAll('a', href=pattern)[0]['href']

    browser.open('https://vm.linevast.de' + '/' + ahref)
    msoup = browser.get_current_page()

    mpattern = re.compile(r'vi:"(.+?)"')
    vi = mpattern.search(str(msoup)).group(1)

    data = {
        'act': 'getstats',
        'vi': vi
    }
    ses = browser.session.post('https://vm.linevast.de/_vm_remote.php', data=data)

    print(ses.status_code == 200)

