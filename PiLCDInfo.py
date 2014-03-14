#!/usr/bin/python

import subprocess
import urllib
import json
import time


class PiLCDInfo:
    host = ''
    port = 4028
    errRate = 0.0
    accepted = 0.0
    hw = 0.0
    diff1shares = 0.0
    uptime = ''
    screen1 = ['no data', 'no data']
    screen2 = ['no data', 'no data']
    currency = 'USD'  # USD GBP EUR JPY AUD CAD CHF CNY DKK HKD PLN RUB SEK SGD THB NOK CZK
    dollars = ['USD', 'AUD', 'CAD']  # currencies with displayable symbols
    last_check = time.time()  # time of last price check
    price_wait = 60.0  # interval between price checks
    price_last = '-'  # last price via mtgox
    price_low = '-'  # low price
    price_high = '-'  # high price

    def __init__(self):
        self.host = self.get_ipaddress()
        self.refresh()
        self.check_price()

    def report_error(self, s):
        self.screen1 = [s, s]
        self.screen2 = [s, s]

    def value_split(self, s):
        r = s.split('=')
        if len(r) == 2: return r
        return r[0], ''

    def response_split(self, s):
        try:
            r = s.split(',')
            title = r[0]
            d = dict(map(self.value_split, r[1:]))
            return title, d
        except ValueError:
            self.report_error('value error')

    def get_ipaddress(self):
        arg = 'ip route list'
        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()
        split_data = data[0].split()
        self.ipaddr = split_data[split_data.index('src') + 1]
        s = '%s' % self.ipaddr
        self.report_error(s)
        return self.ipaddr

    def check_price(self):
        try:
            url = 'https://www.bitstamp.net/api/ticker/'
            f = urllib.urlopen(url)
        except Exception as e:
            self.report_error(e)
            return None
        price_high = None
        price_low = None
        price_last = None

        if f:
            prices_data = f.read()
            try:
                prices_json = json.loads(prices_data)
            except ValueError:
                return None

            if prices_json:
                price_high = prices_json['high']
                price_last = prices_json['last']
                price_low = prices_json['low']

        self.price_last = '$' + price_last if price_last else '-'
        self.price_low = price_low if price_low else '-'
        self.price_high = price_high if price_high else '-'

    def refresh(self):
        now = time.time()
        since = now - self.last_check
        ip_address = self.get_ipaddress()
        if since >= self.price_wait:
            self.check_price()
            self.last_check = time.time()

        self.screen1[0] = 'IP:'
        self.screen1[1] = (ip_address[:15]) if len(ip_address) > 15 else ip_address

        self.screen2[0] = 'last: %s' % self.price_last
        self.screen2[1] = 'H' + self.price_high + ' L' + self.price_low

