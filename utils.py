import smtplib as v
import requests
import os

my_email = "japutest6@gmail.com"
my_password = os.getenv('EMAIL_SENDER_PASSWORD') 

def send_my_letter(email, message):
    with v.SMTP("smtp.gmail.com") as connector:
        connector.starttls()
        connector.login(user=my_email, password=my_password)
        connector.sendmail(from_addr=my_email, to_addrs=email, msg=message)

def fetch_news(query):
    api_token = os.getenv("NEWS_API_TOKEN") 
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_token}&search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("data", [])
        return [{"title": a["title"], "url": a["url"]} for a in articles]
    else:
        return [] 