import subprocess
import schedule
import time

def job():
    subprocess.run(["scrapy", "runspider", "crawler/spiders/xsgd_price_zilswap.py"])
    # subprocess.run(["scrapy", "runspider", "crawler/spiders/xsgd_price_dfx.py"])

schedule.every(20).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
