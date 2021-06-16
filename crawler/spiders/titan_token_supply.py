import scrapy
import telegram
import os.path

class TitanTokenSupplySpider(scrapy.Spider):
    name = 'titan_token_supply'
    allowed_domains = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']
    start_urls = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']

    def parse(self, response):
        response_body = response.body.decode("utf-8")
        start = "id=\"ContentPlaceHolder1_hdnTotalSupply\" value=\""
        start_idx = response_body.rfind(start)
        end = "\" /></div>"
        end_idx = response_body.rfind(end) + 1
        supply_string = response_body[start_idx:end_idx].strip(",")
        supply_float = float(supply_string)

        file = open('titan_token.txt', 'a')
        file.write("{:.15f}\n".format(supply_string))
        file.close()

        file = open('titan_token.txt', 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            v = float(line.strip('\n'))
            d = abs(supply_float - v)
            percentage = (supply_float - v)/supply_float * 100
            if percentage > 3:
                bot = telegram.Bot(token='1774766230:AAFJ8r2cf5P6gidpRgcH8-UGQPYoHrZ0b-8')
                bot.send_message(-542465219, "TITAN token change alert({:.3}%): {:.4f} -> {:.4f}".format(percentage, v, supply_float))
                os.remove('titan_token.txt')
                break
        
        
