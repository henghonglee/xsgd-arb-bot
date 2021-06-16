import scrapy
import telegram

class TitanTokenSupplySpider(scrapy.Spider):
    name = 'titan_token_report_supply'
    allowed_domains = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']
    start_urls = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']

    def parse(self, response):
        response_body = response.body.decode("utf-8")
        start = "id=\"ContentPlaceHolder1_hdnTotalSupply\" value=\""
        start_idx = response_body.rfind(start)
        end = "\" /></div>"
        end_idx = response_body.rfind(end) + 1
        supply_string = response_body[start_idx:end_idx].strip(",")
        bot = telegram.Bot(token='1774766230:AAFJ8r2cf5P6gidpRgcH8-UGQPYoHrZ0b-8')
        bot.send_message(-542465219, "TITAN Supply {:.4f}".format(supply_string))
        
