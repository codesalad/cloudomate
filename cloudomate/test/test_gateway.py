import json
import os
import unittest
import urllib

from mock import MagicMock

from cloudomate.gateway import coinbase, bitpay
from cloudomate.util.bitcoinaddress import validate
from cloudomate.wallet import get_rate


class TestCoinbase(unittest.TestCase):
    # test url from https://developers.coinbase.com/docs/merchants/payment-pages
    TEST_URL = 'https://www.coinbase.com/checkouts/2b30a03995ec62f15bdc54e8428caa87'
    amount = None
    address = None
    rate = None

    @classmethod
    def setUpClass(cls):
        cls.amount, cls.address = coinbase.extract_info(cls.TEST_URL)
        cls.rate = get_rate()

    def test_address(self):
        self.assertTrue(validate(self.address))

    def test_amount(self):
        # default donation is $1, so see if exchange rate is close
        self.assertTrue(0.99 * self.rate < self.amount < 1.01 * self.rate)


class TestBitPay(unittest.TestCase):
    amount = None
    address = None
    rate = None

    @classmethod
    def setUpClass(cls):
        html_file = open(os.path.join(os.path.dirname(__file__), 'resources/bitpay_invoice_data.json'), 'r')
        data = html_file.read()
        json.loads = MagicMock(return_value=json.loads(data))
        cls.amount, cls.address = bitpay.extract_info('https://bitpay.com/invoice?id=4JGT4867vAMLaXUCeezJbG')

    def test_address(self):
        self.assertEqual(self.address, '1C3sb2urF4UZVgEAVcUvHaNyDQjCCQmai3')
        pass

    def test_amount(self):
        print self.amount
        self.assertEqual(self.amount, 0.010511)

    def test_address_valid(self):
        self.assertTrue(validate(self.address))
