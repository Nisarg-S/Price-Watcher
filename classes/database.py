import mysql.connector
import os
from .logger import Logger

logger = Logger('Database')


class Database:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        return mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USERNAME'],
            password=os.environ['MYSQL_PASSWORD'],
            db=os.environ['MYSQL_DB'])

    def insert(self, insertObj: dict) -> int:
        cursor = self.connection.cursor()
        placeholder = ", ".join(["%s"] * len(insertObj))
        insertQuery = "insert into products ({columns}) values ({values});".format(
            columns=",".join(insertObj.keys()), values=placeholder)
        logger.info((insertQuery, list(insertObj.values())))
        cursor.execute(insertQuery, list(insertObj.values()))
        self.connection.commit()
        insertRow = cursor.rowcount
        cursor.close()
        return insertRow

    def checkUniqueURL(self, url: str) -> bool:
        cursor = self.connection.cursor()
        selectQuery = f"SELECT ProductURL from products where ProductURL=\"{url}\""
        logger.info(f"Select Query - {selectQuery}")
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        cursor.close()
        if len(result):
            return False
        else:
            return True

    def getAllProducts(self) -> list:
        cursor = self.connection.cursor()
        selectQuery = f"SELECT * from products"
        logger.info(f"Select Query - {selectQuery}")
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        cursor.close()
        return result

    def updateProduct(self, updateObj: dict, url: str) -> int:
        cursor = self.connection.cursor()
        setValues = ''
        for key, value in updateObj.items():
            setValues += f'{key}="{value}",'
        # [0:-1] for the extra comma
        updateQuery = f"UPDATE products set {setValues[0:-1]} WHERE ProductURL=\"{url}\""
        logger.info(f"Update Query - {updateQuery}")
        cursor.execute(updateQuery)
        result = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return result

    def closeConnection(self):
        self.connection.close()
