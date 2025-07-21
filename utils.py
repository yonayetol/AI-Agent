import os
from dotenv import load_dotenv
import smtplib as v
import requests
from typing import List, Dict

load_dotenv()  # Load environment variables from .env file
 

def send_my_letter(email: str, message: str) -> str:
    """Sends an email to a specified recipient from a default address.

    Args:
        email: The recipient's email address.
        message: The content of the email to be sent.
    
    Returns:
        A confirmation message indicating the email was sent.
    """
    with v.SMTP("smtp.gmail.com") as connector:
        connector.starttls()
        connector.login(user="japutest6@gmail.com", password=os.getenv("EMAIL_SENDER_PASSWORD"))
        connector.sendmail(from_addr="japutest6@gmail.com", to_addrs=email, msg=f"Subject: Message from Metta AI\n\n{message}")
    return "Email sent successfully."

def fetch_news(query: str) -> List[Dict[str, str]]:
    """Fetches news articles from an API based on a search query.

    Args:
        query: The topic to search for news articles about.
        
    Returns:
        A list of dictionaries, where each dictionary represents an article
        and contains a 'title' and a 'url'.
    """
    api_token = os.getenv("NEWS_API_TOKEN")
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_token}&search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("data", [])
        return [{"title": a["title"], "url": a["url"]} for a in articles]
    else:
        return []   