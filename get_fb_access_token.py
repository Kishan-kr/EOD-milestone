import requests

def get_long_lived_user_token(app_id, app_secret, short_user_token) :
  url = f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_user_token}"

  response = requests.get(url)
  long_lived_user_token = response.json()['access_token']
  print('long_lived_user_token: ', long_lived_user_token)


def get_long_lived_page_token(page_id, long_lived_user_token) :
  url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={long_lived_user_token}"

  response = requests.get(url)
  page_access_token = response.json()['access_token']
  print('long_lived_page_token: ', page_access_token)