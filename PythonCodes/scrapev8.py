import re
import pandas as pd

# Load the extracted text file
file_path = "extracted_text.txt"  # Update with actual path
with open(file_path, "r", encoding="utf-8") as file:
    text_lines = file.readlines()

# Define regex patterns
course_pattern = re.compile(r"^\d+\.\d+[A-Za-z]*\s+[A-Za-z]")  # Matches "1.00 Title", "16.381 Title"
invalid_keywords = re.compile(r"\b(provides credit|students|internship|option|information|enrollment|register)\b", re.IGNORECASE)
multi_course_pattern = re.compile(r"(\d+\.\d+[A-Za-z]*\s+or\s+)+\d+\.\d+[A-Za-z]*")  # Matches "16.861 or TPP.21 or 11.200"
metadata_pattern = re.compile(r"\b\d{1,2}-\d{1,2}-\d{1,2}\b")  # Matches unwanted numbers like "2-0-7"
double_space_pattern = re.compile(r"\s{2,}")  # Detects double spaces to truncate the course title

course_titles = []
current_title = ""

for line in text_lines:
    line = line.strip()

    # Check if the line starts with a valid course title
    if course_pattern.match(line) and not invalid_keywords.search(line) and not multi_course_pattern.search(line):
        if current_title:
            course_titles.append(current_title.strip())  # Save the previous title
        current_title = line  # Start a new title

    # Stop processing if we hit "Prereq", "(", or "Information"
    elif current_title and re.search(r"\bprereq|\(|information\b", line, re.IGNORECASE):  
        current_title = re.split(r"prereq|[(]", current_title, flags=re.IGNORECASE)[0].strip()  # Cut at first occurrence
        course_titles.append(current_title)  # Save clean title
        current_title = ""

    # Stop processing if a new course number is detected mid-line
    elif current_title and re.search(r"^\d+\.\d+[A-Za-z]*\b", line):
        course_titles.append(current_title.strip())  # Save current title before a new course starts
        current_title = ""  # Reset

    # Stop processing if metadata-like numbers appear (e.g., "2-0-7")
    elif current_title and metadata_pattern.search(line):
        current_title = metadata_pattern.split(current_title)[0].strip()  # Stop at first occurrence
        course_titles.append(current_title)
        current_title = ""

    # Stop at double spaces which may signify a new line in the title
    elif current_title and double_space_pattern.search(line):
        current_title = double_space_pattern.split(current_title)[0].strip()  # Truncate at double spaces
        course_titles.append(current_title)
        current_title = ""

    elif current_title:
        current_title += " " + line  # Continue building multi-line titles

# Ensure the last captured title is added
if current_title:
    course_titles.append(current_title.strip())

# Convert to DataFrame
df_courses = pd.DataFrame(course_titles, columns=["Course Title"])

# Remove all types of leading and trailing quotes, including Unicode variants
df_courses["Course Title"] = df_courses["Course Title"].str.replace(r'^[“”"]+|[“”"]+$', '', regex=True)

# Display the extracted courses table
print(df_courses)

# Save df_courses to a CSV file
df_courses.to_csv("extracted_course_titles_cleanedv8.csv", index=False, encoding="utf-8")
