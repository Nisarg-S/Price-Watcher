# Price-Watcher

This is a program to track various item prices across Amazon and Newegg.

## Setup

1. To use this program you need a MySQL database set up locally with the following table creation script.

```
CREATE TABLE products(
ProductURL VARCHAR(100) NOT NULL,
ProductNAME VARCHAR(100),
LatestPrice decimal,
LowestPriceAllTime decimal,
LowestPriceMonth decimal,
LowestPriceMonthDate date,
LowestPriceWeek decimal,
LowestPriceWeekDate date,
PRIMARY KEY (ProductURL)
)
```

2. Create a `.env` file from the `.example.env` file and fill in the appropriate values for the environment variables.

3. Then run `insert.py` to add products to the database. You can also set up a batch job to run the file on a recurring basis. For windows users use the `run.bat` file for the batch job. Remember to change the path to the directory.
