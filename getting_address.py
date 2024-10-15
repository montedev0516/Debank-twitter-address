import requests
from bs4 import BeautifulSoup

def get_twitter_address(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific tag with the class "SocialTag_tag__ogpRZ"
        social_tag = soup.find('a', class_='SocialTag_tag__ogpRZ')

        if social_tag and 'href' in social_tag.attrs:
            twitter_address = social_tag['href']
            return twitter_address
        else:
            return "Twitter address not found"

    except requests.RequestException as e:
        return f"An error occurred: {e}"

# URL to scrape
url = "https://debank.com/profile/0x070087acd4830230ed2f56b3abf5e2dcbae55d94"

# Get the Twitter address
twitter_address = get_twitter_address(url)
print(f"Twitter address: {twitter_address}")