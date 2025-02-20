from bs4 import BeautifulSoup
import pandas as pd

def extract_all_courses_from_html(html_file):
    """Extracts all course details from a given BU course HTML file."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find all courses (each course has a <h1> tag for the title)
    courses = soup.find_all("div", id="col1")  # Assuming all courses are under col1

    course_list = []
    
    for course in courses:
        # Extract Course Title
        title = course.find("h1").text.strip() if course.find("h1") else "N/A"

        # Extract Course Code
        code = course.find("h2").text.strip() if course.find("h2") else "N/A"

        # Extract Course Description
        description = "N/A"
        course_content = course.find("div", id="course-content")
        if course_content:
            description_tag = course_content.find("p")
            if description_tag:
                description = description_tag.text.strip()

        # Extract Units
        units = "N/A"
        if course_content:
            units_tag = course_content.find("dt", text="Units:")
            if units_tag:
                units = units_tag.find_next_sibling("dd").text.strip()

        # Extract Course Schedule
        schedule_data = []
        schedule_table = course.find("div", class_="cf-course")
        if schedule_table:
            rows = schedule_table.find_all("tr")[1:]  # Skip table header row
            for row in rows:
                cols = [col.text.strip() for col in row.find_all("td")]
                if len(cols) == 5:  # Ensure correct number of columns
                    schedule_data.append({
                        "Section": cols[0],
                        "Instructor": cols[1],
                        "Location": cols[2],
                        "Schedule": cols[3],
                        "Notes": cols[4]
                    })

        # Append data to course list
        course_list.append({
            "Course Title": title,
            "Course Code": code,
            "Description": description,
            "Units": units,
            "Schedule": schedule_data
        })

    return course_list

# Example usage:
html_file_path = "mergedhtmlsbu.html"  # Change this to your actual file path
courses_data = extract_all_courses_from_html(html_file_path)

# Print result as JSON
import json
print(json.dumps(courses_data, indent=4))

# Save to CSV
all_schedules = []
for course in courses_data:
    for schedule in course["Schedule"]:
        schedule["Course Title"] = course["Course Title"]
        schedule["Course Code"] = course["Course Code"]
        schedule["Units"] = course["Units"]
        all_schedules.append(schedule)

# Save schedule as CSV
df = pd.DataFrame(all_schedules)
df.to_csv("all_courses_schedule.csv", index=False)
print("All course schedules saved to all_courses_schedule.csv")
