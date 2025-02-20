import json
from bs4 import BeautifulSoup

# Load the raw HTML file
html_file = "bu_courses/mergedhtmls.html"  # Update this if needed

with open(html_file, "r", encoding="utf-8") as file:
    raw_html = file.read()

# Parse the HTML
soup = BeautifulSoup(raw_html, "html.parser")

# Find all course sections
courses = soup.find_all("div", id="col1")  # Assuming all courses are under "col1"

parsed_courses = []

for course in courses:
    # Extract Course Title
    title = str(course.find("h1"))  # Store raw HTML
    code = str(course.find("h2"))

    # Extract Course Description
    description = "N/A"
    course_content = course.find("div", id="course-content")
    if course_content and course_content.find("p"):
        description = str(course_content.find("p"))

    # Extract Units
    units = "N/A"
    if course_content:
        units_tag = course_content.find("dt", text="Units:")
        if units_tag:
            units = str(units_tag.find_next_sibling("dd"))

    # Extract Course Schedule
    schedule_data = []
    schedule_table = course.find("div", class_="cf-course")
    if schedule_table:
        rows = schedule_table.find_all("tr")[1:]  # Skip table header row
        for row in rows:
            cols = [str(col) for col in row.find_all("td")]  # Store as raw HTML
            if len(cols) == 5:
                schedule_data.append({
                    "section": cols[0],
                    "instructor": cols[1],
                    "location": cols[2],
                    "schedule": cols[3],
                    "notes": cols[4]
                })

    parsed_courses.append({
        "title": title,
        "code": code,
        "description": description,
        "units": units,
        "schedule": schedule_data
    })

# Save parsed data to JSON file
with open("parsed_courses.json", "w", encoding="utf-8") as file:
    json.dump(parsed_courses, file, indent=4)

print("Parsing complete. Data saved to parsed_courses.json")
