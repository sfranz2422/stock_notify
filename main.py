# Imports
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
# Credentials
load_dotenv('.env')
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.getenv('STOCK_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
TWILLIO_ACCOUNT_SID = os.getenv('TWILLIO_ACCOUNT_SID')
TWILLIO_AUTH_TOKEN = os.getenv('TWILLIO_AUTH_TOKEN')
TO_PHONE = os.getenv('TO_PHONE')
FROM_PHONE = os.getenv('FROM_PHONE')
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    'apikey': STOCK_API_KEY,
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'outputsize': 'compact'
}
def send_message():
    stock_message = f"{new_list} "
    client = Client(TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN)
    message = client.messages.create(
        to=TO_PHONE,
        from_=FROM_PHONE,
        body=stock_message
    )
    print(message.sid)

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
print(response.url)
response.raise_for_status()
# this is one step in...now I have a big dictionary
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_close = data_list[0]['4. close']
previous_close = data_list[1]['4. close']
difference = abs(float(yesterday_close) - float(previous_close))
diff_percent = (difference / float(yesterday_close)) * 100

if diff_percent > 1:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'q': "Tesla"
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    # this is one step in....this is a list of dictionary each item in list is an article
    news_data = news_response.json()["articles"]
    three_stories = news_data[:3]
    new_list = []
    for story in three_stories:
        # new_list = [value for (key, value) in story.items() if key == "title" or key == "description" or key == "url"]
        new_list.append(story['title'])
        new_list.append(story['description'])
        new_list.append(story['url'])
    send_message()
