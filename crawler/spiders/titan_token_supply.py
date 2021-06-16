import scrapy
import telegram
import os.path

class TitanTokenSupplySpider(scrapy.Spider):
    name = 'titan_token_supply'
    allowed_domains = ['https://polygonscan.com/']
    start_urls = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']
    max_retries = 2

    def parse(self, response):
        response_body = response.body.decode("utf-8")
        start = "id=\"ContentPlaceHolder1_hdnTotalSupply\" value=\""
        start_idx = response_body.rfind(start) + len(start)
        end = "\" /></div>"
        end_idx = response_body.rfind(end)
        supply_string = response_body[start_idx:end_idx].replace(',','')
        supply_float = round(float(supply_string), 2)

        file = open('titan_token.txt', 'a')
        file.write("{:.15f}\n".format(supply_float))
        file.close()

        file = open('titan_token.txt', 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            v = float(line.strip('\n'))
            percentage = (supply_float - v)/supply_float * 100
            if percentage > 3:
                bot = telegram.Bot(token='1857941381:AAHPfQwENHSdjxmSyEJt0wutj8PDLZwf81Y')
                bot.send_message(-503777814, "TITAN token change alert({:.3}%): {:.4f} -> {:.4f}".format(percentage, v, supply_float))
                os.remove('titan_token.txt')
                break
        
        
