import re
import pandas as pd

# Load the extracted text file
file_path = "extracted_text.txt"  # Update with actual path
with open(file_path, "r", encoding="utf-8") as file:
    text_lines = file.readlines()

# Define regex pattern for course titles (e.g., "1.00", "2.251J", etc.)
course_pattern = re.compile(r"^\d+\.\d+[A-Za-z]*\s+.+")  # Matches course codes
metadata_pattern = re.compile(r"\b\d{1,2}-\d{1,2}-\d{1,2}\b")  # Matches "2-0-7", "3-1-8" etc.

course_titles = []
current_title = ""

for line in text_lines:
    line = line.strip()

    # Identify a new course title if it matches the regex pattern
    if course_pattern.match(line):
        if current_title:
            course_titles.append(current_title.strip())  # Save the previous title
        current_title = line  # Start a new title

    # Stop processing if the line contains "Prerequisite" or a parenthesis
    elif current_title and ("prereq" in line.lower() or line.startswith("(")):  
        current_title = re.split(r"prereq|[(]", current_title, flags=re.IGNORECASE)[0].strip()  # Cut at "Prerequisite" or "("
        course_titles.append(current_title)  # Save clean title
        current_title = ""

    # Stop processing if the line contains a metadata-like pattern (e.g., "2-0-7")
    elif current_title and metadata_pattern.search(line):
        current_title = metadata_pattern.split(current_title)[0].strip()  # Stop at first occurrence of metadata
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
df_courses.to_csv("extracted_course_titles_cleaned.csv", index=False, encoding="utf-8")
