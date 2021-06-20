import scrapy
import pdb
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

        for line in lines:
            v = float(line.strip('\n'))
            d = abs(rate_usd - v)
            if d > 0.005:
                percentage = (rate_usd - v)/rate_usd * 100
                if rate_usd > 0.755 or rate_usd < 0.71:
                  bot = telegram.Bot(token='1774766230:AAFJ8r2cf5P6gidpRgcH8-UGQPYoHrZ0b-8')
                  bot.send_message(-542465219, "XSGD price alert({:.3}%): {:.4f} -> {:.4f}".format(percentage, v, rate_usd))
                os.remove('xsgd_price.txt')
                break
        
        
