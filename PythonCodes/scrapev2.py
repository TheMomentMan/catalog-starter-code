import pdfplumber
import re
import pandas as pd
import os

# Path to the uploaded PDF
pdf_path = "1996.pdf"

# Define a regex pattern to match course titles (e.g., "1.04 Solid Mechanics", "1.126J Pattern Recognition and Analysis")
course_pattern = re.compile(r"^\d+\.\d+\w*\s+.+")  # Matches course numbers with optional 'J' and title text

# Extract text from pages starting from 4 (as the user mentioned)
course_titles = []

def extract_courses_from_column(column_text):
    current_title = ""
    for line in column_text.split("\n"):
        stripped_line = line.strip().strip('"')
        if course_pattern.match(stripped_line):  # Match lines that fit the course pattern
            if current_title:
                course_titles.append(current_title)
            current_title = stripped_line
        else:
            current_title += " " + stripped_line
    if current_title:
        course_titles.append(current_title)

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[3:]:  # Pages are zero-indexed; start from page 4
        width = page.width
        height = page.height
        left_bbox = (0, 0, width / 3, height)
        middle_bbox = (width / 3, 0, 2 * width / 3, height)
        right_bbox = (2 * width / 3, 0, width, height)

        left_text = page.within_bbox(left_bbox).extract_text()
        middle_text = page.within_bbox(middle_bbox).extract_text()
        right_text = page.within_bbox(right_bbox).extract_text()

        if left_text:
            extract_courses_from_column(left_text)
        if middle_text:
            extract_courses_from_column(middle_text)
        if right_text:
            extract_courses_from_column(right_text)

# Convert to DataFrame for easy visualization
df_courses = pd.DataFrame(course_titles, columns=["Course Title"])

# Display extracted courses
print("Extracted Course Titles:")
print(df_courses)

# Ensure the data directory exists
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the extracted courses to a CSV file
df_courses.to_csv(os.path.join(output_dir, "extracted_courses8.csv"), index=False)