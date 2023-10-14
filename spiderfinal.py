import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def scrape_links(url, max_depth=3, current_depth=1, visited_links=None, result=None):
    if visited_links is None:
        visited_links = set()
    if result is None:
        result = {}

    # Make an HTTP request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and collect links on the page
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Create a dictionary for the current URL
    current_page_links = []

    # Process and append the links
    for link in links:
        absolute_link = urljoin(url, link)
        if absolute_link not in visited_links:
            visited_links.add(absolute_link)
            current_page_links.append(absolute_link)

            # Recursively scrape links up to the specified depth
            if current_depth < max_depth:
                result[absolute_link] = scrape_links(absolute_link, max_depth, current_depth + 1, visited_links, {})

    if current_page_links:
        result[url] = current_page_links

    return result

# Start scraping from the root URL
root_url = 'https://example.com'
scraped_links = scrape_links(root_url)

# Save the result to a JSON file
with open('scraped_links_tree.json', 'w') as json_file:
    json.dump(scraped_links, json_file, indent=4)

print(f'Scraped links and saved in tree structure in "scraped_links_tree.json"')
