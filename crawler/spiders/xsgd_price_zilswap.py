import time
from datetime import datetime
import scrapy
import http.client
import json
import telegram
import os.path

class XsgdPriceSpider(scrapy.Spider):
    name = 'xsgd_price_zilswap'
    allowed_domains = ['https://zilstream.com/tokens/xsgd']
    start_urls = ['https://zilstream.com/tokens/xsgd/']
    

    def parse(self, response):
        response_body = response.body.decode("utf-8")
        start = "{\"props\""
        start_idx = response_body.rfind(start)
        end = "}</script>"
        end_idx = response_body.rfind(end) + 1
        json_response = json.loads(response_body[start_idx:end_idx])
        rate_usd = json_response['props']['pageProps']['token']['rate_usd']

        file = open('xsgd_price.txt', 'a')
        file.write("{:.15f}\n".format(rate_usd))
        file.close()

        file = open('xsgd_price.txt', 'r')
        lines = file.readlines()
        file.close()

        # get api rate regularly
        api_rate = ""
        if os.path.isfile('xsgd_price_fixer.txt'):
          file = open('xsgd_price_fixer.txt', 'r')
          val = file.readline()
          file.close()
          timestamp = float(val.split(';')[1])
          if  time.time() - timestamp < 10800:
            os.remove('xsgd_price_fixer.txt')
            api_rate = 1/self.__get_rate_from_api()
          else: 
            api_rate = val[0]
        else:
          api_rate = 1/self.__get_rate_from_api()
          file = open('xsgd_price_fixer.txt', 'a')
          time_now = str(time.time())
          print(api_rate)
          file.write("{:.15f};{ts}".format(api_rate, ts = time_now))
          file.close()

        for line in lines:
            v = float(line.strip('\n'))
            d = abs(rate_usd - v)
            if d > 0.005:
                percentage = (rate_usd - v)/rate_usd * 100
                if rate_usd > (api_rate/100*102) or rate_usd < (api_rate/100*98):
                  bot = telegram.Bot(token='1774766230:AAFJ8r2cf5P6gidpRgcH8-UGQPYoHrZ0b-8')
                  bot.send_message(-542465219, "XSGD price alert({sym}{:.3}%): {:.3f} -> {:.3f}\nCurrent rate(SGD/USD): {:.5f}".format(percentage, v, rate_usd, api_rate, sym=(u'\U0001f7e2', u'\U0001f534')[percentage < 0]))
                os.remove('xsgd_price.txt')
                break

    def __get_rate_from_api(self):
        conn = http.client.HTTPSConnection("currency23.p.rapidapi.com")
        rate_string = ""
        headers = {
            'x-rapidapi-key': "SFTasPbP2XmshhcVH0KdLQwK9lVGp1r7BxFjsn6fCzskbRs4VF",
            'x-rapidapi-host': "currency23.p.rapidapi.com"
            }
        conn.request("GET", "/currencyToAll?base=USD&int=1", headers=headers)
        res = conn.getresponse()
        price_feed =  json.loads(res.read().decode("utf-8"))
        feeds = price_feed["result"]["data"]
        for feed in feeds:
          if feed['code'] == 'SGD':
            rate_string = feed["rate"]
        return rate_string