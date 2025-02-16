import requests
from bs4 import BeautifulSoup

# Base URL of the MIT Subject Listing & Schedule main page
base_url = 'https://student.mit.edu/catalog/index.cgi'
root_url = 'https://student.mit.edu/catalog/'

# Send a GET request to fetch the content of the main page
response = requests.get(base_url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all anchor tags that link to course pages
course_links = soup.find_all('a', href=True)

# Initialize a list to store the content of each course page
course_contents = []

# Iterate over the found links
for link in course_links:
    href = link['href']
    if href.startswith('m') and href.endswith('.html'):
        course_url = root_url + href
        try:
            # Fetch the content of the course page
            course_response = requests.get(course_url)
            course_response.raise_for_status()
            course_soup = BeautifulSoup(course_response.text, 'html.parser')
            
            # Extract the main content of the course page
            main_content = course_soup.find('body')  # Adjust the tag as needed
            if main_content:
                course_contents.append(str(main_content))
            else:
                print(f"Main content not found in {course_url}")
        except requests.RequestException as e:
            print(f"Failed to fetch {course_url}: {e}")

# Combine all course contents into a single HTML document
combined_html = '<html><head><title>MIT Course Catalog</title></head><body>'
combined_html += ''.join(course_contents)
combined_html += '</body></html>'

# Save the combined HTML to a file
with open('mit_course_catalog.html', 'w', encoding='utf-8') as file:
    file.write(combined_html)

print("Combined HTML file 'mit_course_catalog.html' has been created.")
