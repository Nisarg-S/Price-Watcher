from dotenv import load_dotenv
import datetime
from classes.database import Database
from classes.logger import Logger
from classes.AmazonScraper import AmazonScraper
from classes.neweggScraper import NeweggScraper


def main():
    load_dotenv()
    db = Database()
    db.connect()
    amazonScraper = AmazonScraper()
    neweggScraper = NeweggScraper()
    logger = Logger('Create New Product')
    product = {}
    # logger.info("What is the URL of the product?")
    productURL = input("What is the URL of the product? ")

    isUnique = db.checkUniqueURL(productURL)

    if not isUnique:
        logger.error('ProductURL is aleady setup for scraping')
        return

    # logger.info(
    #     "What is the name of the product (this is just the name you want to give it)?")
    productName = input(
        "What is the name of the product (this is just the name you want to give it)? ")
    if 'amazon' in productURL:
        price = amazonScraper.getPrice(productURL)
    elif 'newegg' in productURL:
        price = neweggScraper.getPrice(productURL)
    product["ProductURL"] = productURL
    product['ProductName'] = productName
    product["LatestPrice"] = price
    product["LowestPriceAllTime"] = price
    product["LowestPriceAllTimeDate"] = datetime.date.today()
    product["LowestPriceMonth"] = price
    product["LowestPriceMonthDate"] = datetime.date.today()
    product["LowestPriceWeek"] = price
    product["LowestPriceWeekDate"] = datetime.date.today()
    product["LastDatePricePulled"] = datetime.date.today()

    db.insert(product)
    db.closeConnection()


if __name__ == "__main__":
    main()
