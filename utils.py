





def send_my_letter(email: str, message: str):
    """Sends an email to the specified address.

    Args:
        email: The recipient's email address.
        message: The content of the email.
    """
    import os
    import smtplib as v
    my_email = os.getenv("EMAIL_SENDER_ADDRESS")
    my_password = os.getenv('EMAIL_SENDER_PASSWORD')

    with v.SMTP("smtp.gmail.com") as connector:
        connector.starttls()
        connector.login(user=my_email, password=my_password)
        connector.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject: A message from Metta\n\n{message}")

def fetch_news(query: str) -> list:
    """Fetches and summarizes news articles based on a query.

    Args:
        query: The search term for the news articles.

    Returns:
        A list of dictionaries, where each dictionary represents a news article
        with a 'title', 'url', and 'summary'.
    """
    import os
    import requests
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
    load_dotenv()

    api_token = os.getenv("NEWS_API_TOKEN")
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_token}&search={query}&limit=3"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []

    articles = response.json().get("data", [])
    summarized_articles = []

    for article in articles:
        try:
            page = requests.get(article["url"])
            soup = BeautifulSoup(page.content, 'html.parser')
            
            # Find all paragraph tags and join their text
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            
            # Create a concise summary (first 3 sentences)
            summary = ". ".join(text.split(". ")[:3]) + "."
            
            summarized_articles.append({
                "title": article["title"],
                "url": article["url"],
                "summary": summary
            })
        except Exception:
            # If scraping fails, just return the title and URL
            summarized_articles.append({
                "title": article["title"],
                "url": article["url"],
                "summary": "Could not summarize this article."
            })
            
    return summarized_articles

def get_weather(location: str) -> dict:
    """Gets the current weather for a given location.

    Args:
        location: The city or zip code to get the weather for.

    Returns:
        A dictionary containing the weather information.
    """
    import os
    import requests
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Could not retrieve weather data."}

def shutdown_pc():
    """Shuts down the computer."""
    import os
    os.system("shutdown /s /t 1")
    return "Shutting down the computer."

def set_alarm(time_str: str):
    """Sets an alarm for a given time.

    Args:
        time_str: The time to set the alarm for, in a format like '10:30am' or '2:00pm'.
    """
    import sched
    import time
    import threading
    from datetime import datetime

    def alarm_action():
        print(f"ALARM! It's {time_str}.")

    try:
        alarm_time = datetime.strptime(time_str, "%I:%M%p")
        now = datetime.now()
        
        alarm_today = alarm_time.replace(year=now.year, month=now.month, day=now.day)
        
        if alarm_today < now:
            # If the time has already passed today, schedule it for tomorrow
            alarm_today = alarm_today.replace(day=now.day + 1)
            
        delay = (alarm_today - now).total_seconds()
        
        s = sched.scheduler(time.time, time.sleep)
        s.enter(delay, 1, alarm_action)
        
        t = threading.Thread(target=s.run)
        t.start()
        
        return f"Alarm set for {time_str}."
    except Exception as e:
        return f"Could not set alarm. Please use a format like '10:30am'. Error: {e}"

def take_screenshot():
    """Takes a screenshot of the entire screen and saves it to a file."""
    try:
        from PIL import ImageGrab
        import time
        import os
        
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
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")