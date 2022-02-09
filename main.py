import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

FROM_ADDRS = os.environ.get("FROM_ADDRS")
PASSWORD = os.environ.get("PASSWORD")
TO_ADDRS = input("For receiving lowest Price notification please enter you E-Mail: \n")
URL = input("Please give the URL of the product: \n")

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Accept-Language": "en-US,en-US;q=0.9,en;q=0.8",
    }
)

product_web_page = response.text
soup = BeautifulSoup(product_web_page, "lxml")

product_price = float(soup.find(name="span", class_="a-offscreen").getText().split("$")[1])
product_title = soup.find(name="span", id="productTitle").getText()


if product_price < 100:
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=FROM_ADDRS, password=PASSWORD)
    connection.sendmail(
        from_addr=FROM_ADDRS,
        to_addrs=TO_ADDRS,
        msg=f"Subject:Amazon Price Alert! \n\n {product_title} now {product_price}\n{URL}"
    )
    connection.close()
