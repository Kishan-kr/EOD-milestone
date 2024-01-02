
import pytz
from scrape_and_store import fetch_all_and_store
from create_image import get_and_create_overlay_image
from post_to_fb import post_image_to_facebook_page
from post_to_twitter import post_on_twitter
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# get env vars 
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# setting image path 
image_path = os.path.join(os.path.dirname(__file__),'.', 'overlay_image.png')

# Indian timezone 
TZ_IST = pytz.timezone('Asia/Kolkata')

# task to generate image and post to socials
def create_image_and_post_to_socials() :
  logging.info('create and post started...')
  # function to fetch all data and store 
  fetch_all_and_store()

  # function call to create image 
  get_and_create_overlay_image()

  # function call to post on fb 
  post_image_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, image_path, 'End Of the Day')

  # function call to post on fb 
  post_on_twitter(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,  image_path, 'End Of the Day')

