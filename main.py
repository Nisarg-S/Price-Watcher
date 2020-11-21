from dotenv import load_dotenv
import datetime
from classes.database import Database
from classes.logger import Logger
from classes.AmazonScraper import AmazonScraper
from classes.notifier import Mailer
from classes.neweggScraper import NeweggScraper


def main():
    allProducts = db.getAllProducts()
    message = ''
    for product in allProducts:
        url = product[0]
        productName = product[1]
        logger.info(f"URL - {url}")
        logger.info(f"Product name - {productName}")
        if 'amazon' in url:
            price = amazonScraper.getPrice(url)
        elif 'newegg' in url:
            price = neweggScraper.getPrice(url)
        logger.info(f"Price - {price}")
        if price == 0:
            logger.error('Amazon Blocked the request')
        else:
            updates = priceProcessing(product, price)
            if 'LowestPriceAlltime' in updates:
                message += f'\nAlltime low price for {productName} at ${price}'
            elif 'LowestPriceMonth' in updates:
                message += f'\nMonthly low price for {productName} at ${price}'
            elif 'LowestPriceWeek' in updates:
                message += f'\nWeekly low price for {productName} at ${price}'

    if message:
        mailer.sendMessage(message)

    db.closeConnection()


def priceProcessing(product: tuple, price: float) -> dict:
    alltimePrice = product[3]
    monthPrice = product[5]
    monthDate = product[6]
    weekPrice = product[7]
    weekDate = product[8]
    updateObj = {}
    now = datetime.date.today()
    updateObj['LatestPrice'] = price
    updateObj['LastDatePricePulled'] = now
    if alltimePrice == 0 or price < alltimePrice:
        updateObj['LowestPriceAlltime'] = price
        updateObj['LowestPriceAlltimeDate'] = now

    delta = now - monthDate
    if monthPrice == 0 or price < monthPrice or delta.total_seconds() > 2.628e6:
        updateObj['LowestPriceMonth'] = price
        updateObj['LowestPriceMonthDate'] = now

    delta = now - weekDate
    if weekPrice == 0 or price < weekPrice or delta.total_seconds() > 604800:
        updateObj['LowestPriceWeek'] = price
        updateObj['LowestPriceWeekDate'] = now

    logger.info(f"{product[1]} - {updateObj}")

    db.updateProduct(updateObj, product[0])
    return updateObj


if __name__ == "__main__":
    load_dotenv()
    db = Database()
    logger = Logger('Scheduled Job')
    amazonScraper = AmazonScraper()
    neweggScraper = NeweggScraper()
    db.connect()
    mailer = Mailer()
    main()
