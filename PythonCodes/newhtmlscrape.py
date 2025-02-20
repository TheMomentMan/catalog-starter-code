import os
import requests
from bs4 import BeautifulSoup

# Base URL
base_url = "https://www.bu.edu"
courses_page_url = "https://www.bu.edu/academics/cas/courses/5/"

# Directory to store downloaded HTML files
output_dir = "bu_courses"
os.makedirs(output_dir, exist_ok=True)

# Fetch the main course listing page
response = requests.get(courses_page_url)
if response.status_code != 200:
    print(f"Failed to fetch main course page. Status code: {response.status_code}")
    exit()

# Parse the course listing page
soup = BeautifulSoup(response.text, "html.parser")

# Extract course links
course_links = []
for link in soup.select("ul.course-feed a"):  # Adjust selector if needed
    href = link.get("href")
    if href and href.startswith("/academics/cas/courses/"):
        course_links.append(base_url + href)

print(f"Found {len(course_links)} course links.")

# Visit each course page and save its full HTML content
for i, course_url in enumerate(course_links):
    print(f"Downloading: {course_url} ({i+1}/{len(course_links)})")

    # Fetch course page content
    course_response = requests.get(course_url)
    if course_response.status_code == 200:
        # Extract course code from URL to name the file
        course_code = course_url.rstrip("/").split("/")[-1]

        # Save full HTML content as a file
        file_path = os.path.join(output_dir, f"{course_code}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(course_response.text)

        print(f"Saved: {file_path}")
    else:
        print(f"Failed to fetch {course_url}, status: {course_response.status_code}")

print(f"All course pages have been downloaded to '{output_dir}/' directory.")
