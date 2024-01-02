import tweepy

def post_on_twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, image_path, tweet_text) :

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create client object from twitter API v2  
    client = tweepy.Client(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)

    # Create API object from twitter API v1 
    api = tweepy.API(auth)

    # function to upload media 
    def upload_image(image):
        try:
            media = api.media_upload(filename= image)
            return media
        except Exception as e:
            print(f"Error occured while uploading image: {e}")
            
    # Function to automate tweet posting (only text)
    def post_tweet(tweet):
        try:
            print(f"Posting tweet: {tweet}")
            response = client.create_tweet(text= tweet)
            print(f"https://twitter.com/user/status/{response.data['id']}")
            print("Tweet posted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Function to post a tweet with an image
    def post_tweet_with_image(text, image_path):
        try:
            # Upload image
            media = upload_image(image_path)

            # Post tweet with image
            response = client.create_tweet(text=text, media_ids=[media.media_id])
            print("Tweeted with image: {}".format(response.data['text']))
        except Exception as e:
            print(f"An error occurred while tweeting: {e}")

    # Path to your image
    # image_path = "overlay_image.png"

    # Tweet text 
    # tweet_text = "Tweet text + image"

    # post_tweet(tweet_text)
    post_tweet_with_image(tweet_text, image_path)


