import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib as v
from PIL import ImageGrab
import time
from datetime import datetime
# Load environment variables once when the script starts
load_dotenv()
 
def send_my_letter(email: str, message: str):
    """Sends an email to the specified address.

    Args:
        email: The recipient's email address.
        message: The content of the email.
    """     
    my_email = os.getenv("EMAIL_SENDER_ADDRESS")
    my_password = os.getenv('EMAIL_SENDER_PASSWORD')
    with v.SMTP("smtp.gmail.com") as connector:
        connector.starttls()
        connector.login(user=my_email, password=my_password)
        connector.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject: A message from All-In-One-Ai-Agent\n\n{message}")

send_my_letter("yonasayeletola62@gmail.com", "Hello, this is a test message from All-In-One-Ai-Agent.")
def fetch_news(query: str) -> list:
    """Fetches and summarizes news articles based on a query.

    Args:
        query: The search term for the news articles.

    Returns:
        A list of dictionaries, where each dictionary represents a news article
        with a 'title', 'url', and 'summary'.
    """
    print(f"Fetching news for query: {query}")
    api_token = os.getenv("NEWS_API_TOKEN")  
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_token}&search={query}&limit=3"
    
    try:
        response = requests.get(url, timeout=60)
    except requests.exceptions.RequestException as e: return []
    print("--------------------------------------------------------------------------------------------------------") # Improved print
    print(f"Response status code: {response}")
    print("--------------------------------------------------------------------------------------------------------") # Improved print
    articles = response.json().get("data", [])
    summarized_articles = [] 

    headers = { # User-Agent for scraping
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for article in articles:
        try:
            # Check if URL exists before attempting to scrape
            if not article.get("url"):
                raise ValueError("Article URL is missing.")

            page = requests.get(article["url"], headers=headers, timeout=55) # Added timeout and headers
            page.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            # Find all paragraph tags and join their text
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs if p.get_text().strip()]) # Added strip to avoid empty strings
            
            # Create a concise summary (first 3 sentences) - basic heuristic
            summary_sentences = [s.strip() for s in text.split(". ") if s.strip()] # Filter empty sentences
            summary = ". ".join(summary_sentences[:3]) + ("." if summary_sentences else "") # Ensure period and handle empty case
            if not summary: # Fallback if no text could be extracted
                summary = "Content could not be extracted for summarization."
            print("--------------------------------------------------------------------------------------------------------") # Improved print
            print("--------------------------------------------------------------------------------------------------------") # Improved print
            print(f"Article: {article}") 
            print("--------------------------------------------------------------------------------------------------------") # Improved print
            print(f"Summarized article: {summary}") # Improved print
            print("--------------------------------------------------------------------------------------------------------") # Improved print
            summarized_articles.append({
                "title": article.get("title", "No Title"), # Use .get with default
                "url": article.get("url", "No URL"),
                "summary": summary
            })
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article '{article.get('title', 'N/A')}': {e}")
            summarized_articles.append({
                "title": article.get("title", "No Title"),
                "url": article.get("url", "No URL"),
                "summary": "Could not fetch or access this article content."
            })
        except Exception as e: # Catch other potential errors during parsing/summary
            print(f"An unexpected error occurred for article '{article.get('title', 'N/A')}': {e}")
            summarized_articles.append({
                "title": article.get("title", "No Title"),
                "url": article.get("url", "No URL"),
                "summary": "Could not summarize this article due to an unexpected error."
            })
    return summarized_articles
# print(fetch_news("trump and musk conflict"))
def get_weather(location: str) -> dict:
    """Gets the current weather for a given location.

    Args:
        location: The city or zip code to get the weather for.

    Returns:
        A dictionary containing the weather information.
    """ 
    print(f"Getting weather for {location}")
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Could not retrieve weather data."}

def shutdown_pc():
    """Shuts down the computer.""" 
    os.system("shutdown /s /t 1")
    return "Shutting down the computer."

def take_screenshot():
    """Takes a screenshot of the entire screen and saves it to a file."""
    try:        
        # Define the directory and create it if it doesn't exist
        save_dir = r"C:\Users\Vertx\Pictures\AI-AGENT-SCREENSHOTS"
        os.makedirs(save_dir, exist_ok=True)
        
        # Create a unique filename
        filename = os.path.join(save_dir, f"screenshot_{int(time.time())}.png")
        
        # Take the screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Could not take screenshot. Error: {e}"

def get_current_time():
    """Gets the current time."""
    return datetime.now().strftime("%I:%M %p")


def restart_pc():
    """Restarts the computer.""" 
    os.system("shutdown /r /t 1")
    return "Restarting the computer."

def lock_pc():
    """Locks the computer.""" 
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Locking the computer."
