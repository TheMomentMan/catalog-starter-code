import requests
from bs4 import BeautifulSoup

# URL of the MIT Subject Listing & Schedule main page
base_url = 'https://student.mit.edu/catalog/index.cgi'

# Send a GET request to fetch the content of the page
response = requests.get(base_url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all anchor tags that link to course pages
course_links = soup.find_all('a', href=True)

# Initialize a set to store unique URL suffixes
url_suffixes = set()

# Iterate over the found links
for link in course_links:
    href = link['href']
    if href.startswith('m') and href.endswith('.html'):
        url_suffixes.add(href)

# Print the extracted URL suffixes
for suffix in sorted(url_suffixes):
    print(suffix)
