import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
import logging
from datetime import datetime, timedelta
from pymongo import MongoClient
from datetime import datetime, timedelta
from requests.exceptions import RequestException
import pytz

# IST timezone
TZ_IST = pytz.timezone('Asia/Kolkata')

# Constants
MONGODB_CONNECTION_STRING = (
    "mongodb+srv://milestonegpt4:kv6A5KW7sUKJ9jOQ@cluster0.krug8nd.mongodb.net/"
)

LOG_FILE = "app.log"

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler(LOG_FILE)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
file_handler.setFormatter(file_formatter)

# Create a console handler for printing logs to the console
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logging.info("This log will appear in both the console and the file.")

# MongoDB Setup
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.Milestone  # database name
collection = db.FinData  # collection name

# Constants
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


def get_data_from_url(url):
    headers = {"User-Agent": USER_AGENT}
    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.info(f"HTTP request error: {e}")
        return None


# Modify the get_nifty_50_values() function to return a dictionary
def get_nifty_50_values():
    """To get Nifty 50 value from Moneycontrol.com"""
    response = get_data_from_url(
        "https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Today's Value
        todays_value_element = soup.find("input", {"id": "spotValue"})
        todays_value = todays_value_element["value"] if todays_value_element else "N/A"

        # Change and Change Direction
        change_div = soup.find("div", {"id": "sp_ch_prch"})
        if change_div:
            change_text = change_div.get_text(strip=True).split("(")[0]
            change_direction = "down" if "red" in change_div["class"] else "up"
        else:
            change_text = "N/A"
            change_direction = "N/A"

        # Previous Close
        try:
            previous_close = "{:,.2f}".format(
                float(todays_value.replace(",", ""))
                - float(change_text.replace(",", ""))
            )
        except ValueError:
            previous_close = "N/A"
        logging.info(f"NIFTY 50 Todays: {todays_value}, prev: {previous_close}")
        return {
            "Symbol": "Nifty50",
            "spot": todays_value,
            "prev": previous_close,
            "change": change_text,
        }
    else:
        logging.info("Failed to fetch data. Status code:", response.status_code)
        return {"Symbol": "Nifty50", "spot": "N/A", "prev": "N/A", "change": "N/A"}


def get_india_vix_values():
    response = get_data_from_url(
        "https://www.moneycontrol.com/indian-indices/india-vix-36.html"
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Today's Value
        todays_value_element = soup.find("input", {"id": "spotValue"})
        todays_value = todays_value_element["value"] if todays_value_element else "N/A"

        # Change and Change Direction
        change_div = soup.find("div", {"id": "sp_ch_prch"})
        if change_div:
            change_text = change_div.get_text(strip=True).split("(")[0]
            change_direction = "down" if "red" in change_div["class"] else "up"
        else:
            change_text = "N/A"
            change_direction = "N/A"
        logging.info(
            f"INDIA VIX: Todays: {todays_value}, change: {change_text}, dir: {change_direction}"
        )
        return {
            "Symbol": "IndiaVix",
            "spot": todays_value,
            "change": change_text,
            "changedir": change_direction,
        }
    else:
        logging.info(
            "Failed to fetch India VIX data. Status code:", response.status_code
        )
        return {
            "Symbol": "IndiaVix",
            "spot": "N/A",
            "change": "N/A",
            "changedir": "N/A",
        }


# Modify the get_sensex_values() function to return a dictionary
def get_sensex_values():
    """To get Sensex value from Moneycontrol.com"""
    response = get_data_from_url(
        "https://www.moneycontrol.com/indian-indices/sensex-4.html"
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Today's Value
        todays_value_element = soup.find("input", {"id": "spotValue"})
        todays_value = todays_value_element["value"] if todays_value_element else "N/A"

        # Change and Change Direction
        change_div = soup.find("div", {"id": "sp_ch_prch"})
        if change_div:
            change_text = change_div.get_text(strip=True).split("(")[0]
            change_direction = "down" if "red" in change_div["class"] else "up"
        else:
            change_text = "N/A"
            change_direction = "N/A"

        # Previous Close
        try:
            previous_close = "{:,.2f}".format(
                float(todays_value.replace(",", ""))
                - float(change_text.replace(",", ""))
            )
        except ValueError:
            previous_close = "N/A"
        logging.info(
            f"SENSEX: Todays: {todays_value}, prev: {previous_close}, change: {change_text}"
        )
        return {
            "Symbol": "Sensex",
            "spot": todays_value,
            "prev": previous_close,
            "change": change_text,
        }
    else:
        logging.info("Failed to fetch data. Status code:", response.status_code)
        return {"spot": "N/A", "prev": "N/A", "change": "N/A"}


def get_gold_values():
    response = get_data_from_url("https://www.91mobiles.com/finance/gold-rate-in-delhi")
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        gold_price_divs = soup.find_all(
            "div", {"class": "pricebox"}
        )  # Adjusted to match the new source's structure

        for div in gold_price_divs:
            gold_price_span = div.find("span", {"class": "c-prc"})
            if gold_price_span:
                gold_price_text = (
                    gold_price_span.get_text(strip=True)
                    .replace("₹", "")
                    .replace(",", "")
                )
                ##logging.info(f"Extracted gold price text: {gold_price_text}")  # Logging the extracted text

                match = re.search(
                    r"\d+\.?\d*", gold_price_text
                )  # Adjusted regex to match the format
                if match:
                    gold_price = match.group()
                    logging.info(f"Gold Price Today: {gold_price}")
                    return {"GoldPrice": "{:,.2f}".format(float(gold_price))}
                else:
                    logging.info("Gold price format not recognized.")
                    return None

        logging.info("Gold price span not found.")
        return None
    else:
        logging.error(
            f"Failed to fetch gold data. Status code: {response.status_code if response else 'No response'}"
        )
        return None


def get_silver_values():
    url = "https://www.91mobiles.com/finance/silver-rate-in-delhi"

    response = get_data_from_url(url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        silver_price_tables = soup.find_all("table", class_="history-table")

        for table in silver_price_tables:
            silver_price_row = table.find("tbody").find(
                "tr"
            )  # Assuming the first row contains the latest price
            if silver_price_row:
                silver_price_data = silver_price_row.find_all("td")
                if silver_price_data and len(silver_price_data) > 3:
                    silver_price_1kg = (
                        silver_price_data[3]
                        .get_text(strip=True)
                        .replace("₹", "")
                        .replace(",", "")
                    )
                    ##logging.info(f"Extracted silver price text for 1 kg: {silver_price_1kg}")

                    match = re.search(r"\d+\.?\d*", silver_price_1kg)
                    if match:
                        silver_price = match.group()
                        logging.info(f"Silver Price Today: {silver_price}")
                        return {"SilverPrice": "{:,.2f}".format(float(silver_price))}
                    else:
                        logging.info("Silver price format not recognized.")
                        return None
                else:
                    logging.info("Silver price data not found.")
                    return None
            else:
                logging.info("Silver price row not found.")
                return None
        logging.info("Silver price table not found.")
        return None
    else:
        logging.error(
            f"Failed to fetch silver data. Status code: {response.status_code if response else 'No response'}"
        )
        return None


def get_fii_values():
    logging.info("Getting FII Values")
    url = "https://web.stockedge.com/fii-activity?section=cm-provisional&time-span=monthly"
    data = {"current_month_value": None, "prev_month_value": None}
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.find_all("ion-text", class_="md hydrated")

        if len(items) > 0:
            data["current_month_value"] = items[0].get_text(strip=True)
        if len(items) > 3:
            data["prev_month_value"] = items[3].get_text(strip=True)

    except NoSuchElementException:
        logging.error("Element not found while trying to scrape FII data.")
    except TimeoutException:
        logging.error("Timeout occurred while trying to scrape FII data.")
    except WebDriverException as e:
        logging.error(f"Webdriver error occurred: {e}")
    finally:
        driver.quit()

    # logging.info(f"FII Current Month Value: {data['current_month_value']}")
    # logging.info(f"FII Previous Month Value: {data['prev_month_value']}")
    return {
        "symbol": "FII",
        "CurrentMonth": data["current_month_value"],  # Assuming it's a scalar value
        "PreviousMonth": data["prev_month_value"],
    }


def get_dii_values():
    logging.info("Getting DII Values")
    url = "https://web.stockedge.com/fii-activity?section=cm-provisional&time-span=monthly&fii-dii-type=dii"
    data = {"current_month_value": None, "prev_month_value": None}
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.find_all("ion-text", class_="md hydrated")

        if len(items) > 0:
            data["current_month_value"] = items[0].get_text(strip=True)
        if len(items) > 3:
            data["prev_month_value"] = items[3].get_text(strip=True)

    except NoSuchElementException:
        logging.error("Element not found while trying to scrape DII data.")
    except TimeoutException:
        logging.error("Timeout occurred while trying to scrape DII data.")
    except WebDriverException as e:
        logging.error(f"Webdriver error occurred: {e}")
    finally:
        driver.quit()

    # logging.info(f"DII Current Month Value: {data['current_month_value']}")
    # logging.info(f"DII Previous Month Value: {data['prev_month_value']}")
    return {
        "symbol": "DII",
        "CurrentMonth": data["current_month_value"],  # Assuming it's a scalar value
        "PreviousMonth": data["prev_month_value"],
    }


def get_conversion_rates():
    url = "https://currency-converter-pro1.p.rapidapi.com/convert"
    headers = {
        "X-RapidAPI-Key": "ae2760dcf1msh1bf9f8761a67590p1cc8e6jsn36ea107d8ae7",
        "X-RapidAPI-Host": "currency-converter-pro1.p.rapidapi.com",
    }

    usd_inr_querystring = {"from": "USD", "to": "INR", "amount": "1"}
    eur_inr_querystring = {"from": "EUR", "to": "INR", "amount": "1"}

    usd_inr_response = requests.get(url, headers=headers, params=usd_inr_querystring)
    eur_inr_response = requests.get(url, headers=headers, params=eur_inr_querystring)

    usd_inr_rate = None
    eur_inr_rate = None

    if usd_inr_response.status_code == 200 and isinstance(
        usd_inr_response.json(), dict
    ):
        usd_inr_rate = round(usd_inr_response.json().get("result", 0), 2)

    if eur_inr_response.status_code == 200 and isinstance(
        eur_inr_response.json(), dict
    ):
        eur_inr_rate = round(eur_inr_response.json().get("result", 0), 2)

    logging.info(f"USD to INR Conversion Rate: {usd_inr_rate}")
    logging.info(f"EUR to INR Conversion Rate: {eur_inr_rate}")
    return usd_inr_rate, eur_inr_rate


def get_interest_rate_for_india(max_retries=3):
    api_url = "https://api.api-ninjas.com/v1/interestrate?country=india"
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(
                api_url,
                headers={"X-Api-Key": "K/PS+uWvhvu1M8OZCDG3rg==LXwgZTbDrDfA1L9d"},
            )
            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                logging.error(
                    f"Attempt {attempt + 1}: Error fetching rates - {response.status_code} {response.text}"
                )
        except RequestException as e:
            logging.error(
                f"Attempt {attempt + 1}: Exception in get_interest_rate_for_india: {e}"
            )

        attempt += 1
        logging.info(f"Retrying... Attempt {attempt + 1}")

    logging.error("Max retries reached. Failed to fetch interest rates.")
    return None


def extract_required_rates(interest_rate_data):
    if not interest_rate_data:
        return None

    # Extracting Central Bank Rate
    central_bank_rates = interest_rate_data.get("central_bank_rates", [])
    central_bank_rate = central_bank_rates[0] if central_bank_rates else None

    # Extracting Non-Central Bank Rates
    non_central_bank_rates = interest_rate_data.get("non_central_bank_rates", [])

    usd_libor = next(
        (
            item
            for item in non_central_bank_rates
            if item["name"] == "USD LIBOR - 1 month"
        ),
        None,
    )
    eur_libor = next(
        (
            item
            for item in non_central_bank_rates
            if item["name"] == "Euribor - 1 month"
        ),
        None,
    )  # Adjust this if the name is different
    sofr = next(
        (item for item in non_central_bank_rates if item["name"] == "SOFR"), None
    )

    return {
        "central_bank_rate": central_bank_rate,
        "usd_libor": usd_libor,
        "eur_libor": eur_libor,
        "sofr": sofr,
    }


def historicalRate(currency_from):
    try:
        # Calculate yesterday's date
        yesterday = datetime.now() - timedelta(days=1)
        formatted_date = yesterday.strftime("%Y-%m-%d")

        # API URL
        url = f"https://currency-converter5.p.rapidapi.com/currency/historical/{formatted_date}"

        querystring = {
            "from": currency_from,
            "amount": "1",
            "format": "json",
            "to": "INR",
            "language": "en",
        }

        headers = {
            "X-RapidAPI-Key": "ae2760dcf1msh1bf9f8761a67590p1cc8e6jsn36ea107d8ae7",
            "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            logging.info(response.json())
            return response.json()
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {e}"


# Use usd_inr_rate_yesterday and eur_inr_rate_yesterday as needed


def store_data_in_mongodb(data_list):
    try:
        # Consolidate data into a single dictionary
        consolidated_data = {}
        for data in data_list:
            if isinstance(data, dict):
                consolidated_data.update(data)

        # get current local time 
        local_time = datetime.now()

        # convert local time to IST 
        ist_time = local_time.astimezone(TZ_IST)

        # Add a timestamp
        consolidated_data["timestamp"] = ist_time

        # Insert the consolidated data as a single document
        collection.insert_one(consolidated_data)
        logging.info("Consolidated data stored in MongoDB successfully")
    except Exception as e:
        logging.error(f"Error storing consolidated data in MongoDB: {e}")


def clean_old_data(collection):
    try:
        # Define the cutoff time as yesterday
        cutoff_time = datetime.now() - timedelta(days=1)

        # Delete documents older than yesterday
        deletion_result = collection.delete_many({"timestamp": {"$lt": cutoff_time}})
        logging.info(
            f"Deleted {deletion_result.deleted_count} old records from MongoDB."
        )
    except Exception as e:
        logging.error(f"Error cleaning old data from MongoDB: {e}")


def fetch_all_and_store():
    try:
        # Fetch data
        usd_inr_rate_yesterday = historicalRate("USD")
        interest_rate_data = get_interest_rate_for_india()
        nifty_data = get_nifty_50_values()
        sensex_data = get_sensex_values()
        india_vix_data = get_india_vix_values()  
        gold_data = get_gold_values()
        silver_data = get_silver_values()
        usd_inr_rate, eur_inr_rate = get_conversion_rates()
        fii_data = get_fii_values()
        dii_data = get_dii_values()
        india_interest_rate = extract_required_rates(interest_rate_data)
        eur_inr_rate_yesterday = historicalRate("EUR")

        # Prepare the data list
        data_list = [
            {"nifty_data": nifty_data},
            {"sensex_data": sensex_data},
            {"india_vix_data": india_vix_data},
            {"gold_price": gold_data},  # Converting to dictionary
            {"silver_price": silver_data},  # Converting to dictionary
            {"usd_inr_rate": usd_inr_rate, "eur_inr_rate": eur_inr_rate},
            {"fii_data":fii_data},
            {"dii_data":dii_data},
            {"india_interest_rate":india_interest_rate},
            {"usd_historical": usd_inr_rate_yesterday},
            {"eur_historical": eur_inr_rate_yesterday},
        ]
        print(data_list)
        # Store all data
        clean_old_data(collection)
        store_data_in_mongodb(data_list)

        logging.info("Data processing and storage cycle completed")
    except Exception as e:
        logging.error(f"Error in main loop: {e}")

