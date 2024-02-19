import requests
import pandas as pd
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

AV_API_KEY = "YOUR OWN API"
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

alphavantage_url = 'https://www.alphavantage.co/query'
alphavantage_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": AV_API_KEY,
}

r = requests.get(alphavantage_url, params=alphavantage_parameter)
data = r.json()

sample_data = data["Time Series (Daily)"]

sample_data = pd.DataFrame.from_dict(sample_data, orient="index")
df = sample_data.head(2)
print(df)

ALERT_PERCENTAGE_CHANGE = 0.1

last_close = float(df.iloc[0]["4. close"])
previous_close = float(df.iloc[1]["4. close"])

rate_change = round((last_close - previous_close) / previous_close * 100, 3)

if abs(rate_change) >= ALERT_PERCENTAGE_CHANGE:
    print(f"Stock price changed {rate_change}%.\nAlarm trigger % change is {ALERT_PERCENTAGE_CHANGE}%\nGET NEWS.")
    get_news = True


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# News API
NEWS_API_KEY = "YOUR OWN API KEY"

# TWILIO
account_sid = "YOUR OWN SID"
auth_token = "YOUR OWN TOKEN"
client = Client(account_sid, auth_token)

if get_news: 
       date = date.today() - timedelta(3)
       print(date)
       news_url = ('https://newsapi.org/v2/everything?'
              f'q={COMPANY_NAME}&'
              f'from={date}&'
              'sortBy=relevancy&'
              f'apiKey={NEWS_API_KEY}')
       response = requests.get(news_url)

top_news = response.json()["articles"][0:3]
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
if rate_change >= 0:
    up_down = "🔺"
else: up_down = "🔻"
    
for news in top_news:
    msg = f"{STOCK}: {up_down}{rate_change}\nHeadlne: {news['title']}\nBrief: {top_news[0]['description']}\nLink: {news['url']}"
    print(msg)
    message = client.messages \
            .create(
                 body=msg,
                 from_='Phone Number',
                 to='Phone Number'
             )

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""