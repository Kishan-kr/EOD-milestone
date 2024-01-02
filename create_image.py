import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from pymongo import MongoClient

# Constants from your provided code
MONGODB_CONNECTION_STRING = "mongodb+srv://milestonegpt4:kv6A5KW7sUKJ9jOQ@cluster0.krug8nd.mongodb.net/"
DB_NAME = "Milestone"  # Database name from your code
COLLECTION_NAME = "FinData"  # Collection name from your code
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
FONT_PATH = 'C:\\Windows\\Fonts\\FRAMD.ttf'  # Update this path as per your system

# MongoDB Setup
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
    
# List of background images
BACKGROUND_IMAGES = [
    "https://niveshonline.com/public/EOD%20website/background1.png",
    "https://niveshonline.com/public/EOD%20website/background2.png",  
    "https://niveshonline.com/public/EOD%20website/background3.png",
    "https://niveshonline.com/public/EOD%20website/background4.png",
    "https://niveshonline.com/public/EOD%20website/background5.png",
]

# Function to randomly select a background image URL
def get_random_background_url(previous_url=None):
    available_images = [image for image in BACKGROUND_IMAGES if image != previous_url]
    return random.choice(available_images)


# changes made start 
def get_latest_financial_data():
    try:
        latest_data = collection.find().sort("timestamp", -1).limit(1)
        return latest_data[0] if latest_data else None
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        return None
# changes made end 

def fetch_background_image(url):
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching background image: {e}")
        return None

# function to format to two digit 
def get_two_digit(value):
    value = float(value)
    return f"{value:.2f}"

def get_change_value(current, previous):
    try:
        change = float(current) - float(previous)
        return f"{change:.2f}"  # Format with two decimal places
    except ValueError:
        return "N/A"  # Return 'N/A' if conversion fails
    
# Function to determine the color based on the change
def get_change_color(change_value):
    try:
        return (0, 255, 0) if float(change_value) >= 0 else (255, 0, 0)
    except ValueError:
        return (0, 0, 0)
    
def get_and_create_overlay_image():
    # Define the path to the overlay image
    overlay_image_path = "overlay_image.png"

    # Check if the overlay image exists, and delete it if it does
    if os.path.exists(overlay_image_path):
        try:
            os.remove(overlay_image_path)
            print("Previous overlay image deleted.")
        except Exception as e:
            print(f"Error deleting previous overlay image: {e}")

    # Fetch data for overlay
    financial_data = get_latest_financial_data()
    if not financial_data:
        print("No financial data available.")
        return
    
    # Get the previously used background URL from a file (if available)
    try:
        with open("previous_background.txt", "r") as file:
            previous_background_url = file.read().strip()
    except FileNotFoundError:
        previous_background_url = None

    # Extract data from the financial_data dictionary
    nifty_data = financial_data.get('nifty_data', {})
    sensex_data = financial_data.get('sensex_data', {})
    india_vix_data = financial_data.get('india_vix_data', {})
    gold_data = financial_data.get('gold_price', {})
    silver_data = financial_data.get('silver_price', {})
    conversion_data = {
        "usd_inr_rate": financial_data.get('usd_inr_rate', {}),
        "eur_inr_rate": financial_data.get('eur_inr_rate', {}),
        "prev_usd_inr_rate": financial_data['usd_historical'].get('rates', {}).get('INR', {}).get('rate', None),
        "prev_eur_inr_rate": financial_data['eur_historical'].get('rates', {}).get('INR', {}).get('rate', None)
    } # changes made
    fii_data = financial_data.get('fii_data', {})
    dii_data = financial_data.get('dii_data', {})

     # Randomly select a background image URL
    background_url = get_random_background_url(previous_background_url)

     # Save the current background URL for future reference
    with open("previous_background.txt", "w") as file:
        file.write(background_url)

    # Call the function to create overlay image
    create_overlay_image(nifty_data, sensex_data, india_vix_data, gold_data, silver_data, conversion_data, fii_data, dii_data, background_url)

def create_overlay_image(nifty_data, sensex_data, india_vix_data, gold_data, silver_data, conversion_data, fii_data, dii_data, background_url):
    try:
        # Fetch background image
        background_response = requests.get(background_url, headers={"User-Agent": USER_AGENT})
        background_response.raise_for_status()  # Ensure the request was successful
        background_image = Image.open(BytesIO(background_response.content))
        font_size = 20
        font = ImageFont.truetype(FONT_PATH, font_size)
        text_color = (255, 255, 255)
        draw = ImageDraw.Draw(background_image)

        font_path = 'C:\\Windows\\Fonts\\FRAMD.ttf'
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        text_color = (255, 255, 255)
        draw = ImageDraw.Draw(background_image)

        # Add the date overlay code here
        current_date = datetime.now().strftime('%d %B %Y')

        # First location
        date_position1 = (850, 348)  # Replace x1 and y1 with your desired coordinates
        draw.text(date_position1, current_date, fill=text_color, font=font)

        # Second location
        date_position2 = (850, 30)  # Replace x2 and y2 with your desired coordinates
        draw.text(date_position2, current_date, fill=text_color, font=font)

        # Third location
        date_position3 = (850, 218)  # Replace x3 and y3 with your desired coordinates
        draw.text(date_position3, current_date, fill=text_color, font=font)

        
        # Determine the color for nifty 50 change based on spot and prev values
        nifty_change_color = get_change_color(nifty_data['change'])

        # Determine the color for sensex change based on spot and prev values
        sensex_change_color = get_change_color(sensex_data['change'])

        # changes made start 
        # Determine the color for usd to inr change
        usd_inr_change_value = get_change_value(conversion_data.get('usd_inr_rate'), conversion_data.get('prev_usd_inr_rate'))
        usd_inr_change_color = get_change_color(usd_inr_change_value)
        print("usd inr change value: ", usd_inr_change_value) #test

        # Determine the color for eur to inr change
        eur_inr_change_value = get_change_value(conversion_data.get('eur_inr_rate'), conversion_data.get('prev_eur_inr_rate'))
        eur_inr_change_color = get_change_color(eur_inr_change_value)
        # changes made end 

        nifty50_positions = {
            f"  {nifty_data['spot']}": (790, 103),
            f"  {nifty_data['prev']}": (585, 103),
            f"  {nifty_data['change']}": (995, 103),
        }

        sensex_positions = {
            f"  {sensex_data['spot']}": (790, 145),
            f"  {sensex_data['prev']}": (585, 145),
            f"  {sensex_data['change']}": (995, 145),
        }

        india_vix_positions = {
            f"  {india_vix_data['spot']}": (595, 180),
        }

        gold_positions = {
            f"  {gold_data['GoldPrice']}": (585, 382)
        }

        silver_positions = {
            f"  {silver_data['SilverPrice']}": (585, 415)
        }

        conversion_positions = {
            f" {conversion_data.get('usd_inr_rate', 'N/A')}": (820, 282),
            f" {conversion_data.get('eur_inr_rate', 'N/A')}": (820, 312),
            f" {get_two_digit(conversion_data.get('prev_usd_inr_rate', 'N/A'))}": (595, 282),
            f" {get_two_digit(conversion_data.get('prev_eur_inr_rate', 'N/A'))}": (595, 312),
        }

        # change added start
        conversion_change_positions = {
            f" {usd_inr_change_value}": (995, 282),
            f" {eur_inr_change_value}": (995, 312)
        }
        # changes added end 

        fii_positions = {
            f" {fii_data['CurrentMonth']}": (800, 498),
            f" {fii_data['PreviousMonth']}": (800, 526),
        }

        dii_positions = {
            f" {dii_data['CurrentMonth']}": (980, 498),
            f" {dii_data['PreviousMonth']}": (980, 526),
        }

        text_and_positions = {**nifty50_positions, **sensex_positions, **india_vix_positions, **gold_positions, **silver_positions, **conversion_positions, **conversion_change_positions, **fii_positions, **dii_positions}

        for text, position in text_and_positions.items():
            if position == nifty50_positions[f"  {nifty_data['change']}"]:
                draw.text(position, text, fill=nifty_change_color, font=font)
            elif position == sensex_positions[f"  {sensex_data['change']}"]:
                draw.text(position, text, fill=sensex_change_color, font=font)

            # changes made start 
            elif position == conversion_change_positions[f" {usd_inr_change_value}"]:
                draw.text(position, text, fill=usd_inr_change_color, font=font)
            elif position == conversion_change_positions[f" {eur_inr_change_value}"]:
                draw.text(position, text, fill=eur_inr_change_color, font=font)
            # changes made end 

            elif "change" in text.lower() and not text.startswith("N/A"):
                change_value = float(text.split()[-1].replace(",", ""))
                if change_value > 0:
                    change_color = (0, 255, 0)  # Set text color to green for positive change
                else:
                    change_color = (255, 0, 0)  # Set text color to red for negative change
                draw.text(position, text, fill=change_color, font=font)
            else:
                draw.text(position, text, fill=text_color, font=font)

        background_image.save("overlay_image.png")
        print("Overlay image created successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching background image: {e}")
    except Exception as e:
        print(f"An error occurred in create_overlay_image: {e}")

# Call the function to get data and create an overlay image
# get_and_create_overlay_image()