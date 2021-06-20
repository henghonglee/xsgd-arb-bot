import subprocess
import schedule
import time

def job():
    subprocess.run(["scrapy", "runspider", "crawler/spiders/xsgd/xsgd_price_zilswap.py"])
    # subprocess.run(["scrapy", "runspider", "crawler/spiders/iron_finance/titan_token_supply.py"])
    # subprocess.run(["scrapy", "runspider", "crawler/spiders/iron_finance/iron_token_supply.py"])

schedule.every(20).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
