





def send_my_letter(email: str, message: str):
    """Sends an email to the specified address.

    Args:
        email: The recipient's email address.
        message: The content of the email.
    """
    import os
    import smtplib as v
    my_email = "japutest6@gmail.com"
    my_password = os.getenv('EMAIL_SENDER_PASSWORD')

    with v.SMTP("smtp.gmail.com") as connector:
        connector.starttls()
        connector.login(user=my_email, password=my_password)
        connector.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject: A message from Metta\n\n{message}")

def fetch_news(query: str) -> list:
    """Fetches news articles based on a query.

    Args:
        query: The search term for the news articles.

    Returns:
        A list of dictionaries, where each dictionary represents a news article
        with a 'title' and a 'url'.
    """
    from serpapi import GoogleSearch

    params = {
    "engine": "google_news",
    "q": query,
    "gl": "us",
    "hl": "en",
    "api_key": "1bb77ac8497594f5a53085865dd865c747867366c80ee63ad4ffc58da05c35a3"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    news_results = results["news_results"]

    for _ in range(100):print("hi")
    
    return news_results
    import os
    import requests
    from dotenv import load_dotenv
    load_dotenv()

    api_token = os.getenv("NEWS_API_TOKEN")
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_token}&search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("data", [])
        return [{"title": a["title"], "url": a["url"]} for a in articles]
    else:
        return []