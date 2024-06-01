# Import necessary modules
import requests
from bs4 import BeautifulSoup

# Define a function to fetch Pinterest images for a given query
def get_pinterest_images(query):
    try:
        # Construct the Pinterest search URL
        url = f"https://id.pinterest.com/search/pins/?autologin=true&q={query}"
        
        # Send a GET request to the Pinterest search URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
        
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all image links in the search results
        image_links = soup.select('div > a img')
        
        # Extract the src attribute of each image link
        image_urls = [link['src'] for link in image_links if 'src' in link.attrs]
        
        return image_urls
    except Exception as e:
        print(f"An error occurred while fetching Pinterest images: {e}")
        return []

# Example usage:
# images = get_pinterest_images("anime pfp")
# print(images)
