import scrapy
from scrapy.selector import Selector
import telegram

class TitanTokenSupplySpider(scrapy.Spider):
    name = 'titan_token_report_supply'
    allowed_domains = ['polygonscan.com/']
    start_urls = ['https://polygonscan.com/token/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a']
    max_retries = 2
    
    def parse(self, response):
        response_body = response.body.decode("utf-8")
        start = "id=\"ContentPlaceHolder1_hdnTotalSupply\" value=\""
        start_idx = response_body.rfind(start) + len(start)
        end = "\" /></div>"
        end_idx = response_body.rfind(end)
        supply_string = response_body[start_idx:end_idx].replace(',','')
        supply_val = float(supply_string)
        print(supply_val)

        request = scrapy.Request('https://polygonscan.com/token/generic-tokenholders2?m=normal&a=0xaaa5b9e6c589642f98a1cda99b9d024b8407285a&s=104658925627917937125433346&p=1',
                             callback=self.parse_page2,
                             cb_kwargs=dict(main_url=response.url),
                             dont_filter=True)
        request.cb_kwargs['supply_val'] = supply_val  # add more arguments for the callback
        yield request
        
    def parse_page2(self, response, main_url, supply_val):
        bank_supply_string = response.xpath("//*[@id=\"maintable\"]/div[3]/table/tbody/tr[1]/td[3]/text()").getall()[0].replace(',','')
        bank_supply_val = float(bank_supply_string)
        circ_supply_val = supply_val - bank_supply_val
        percentage = (circ_supply_val / supply_val) * 100
        bot = telegram.Bot(token='1857941381:AAHPfQwENHSdjxmSyEJt0wutj8PDLZwf81Y')
        bot.send_message(-503777814, "TITAN Circulating Supply {:,} ({:.3f}%)".format(circ_supply_val, percentage))
        