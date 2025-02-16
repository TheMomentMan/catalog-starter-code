import pdfplumber
import re
import pandas as pd

# Path to the uploaded PDF
pdf_path = "1996.pdf"

# Define a regex pattern to match course titles (e.g., "1.04 Solid Mechanics", "1.126J Pattern Recognition and Analysis")
course_pattern = re.compile(r"^\d+\.\d+\w*\s+.+")  # Matches course numbers with optional 'J' and title text

# Extract text from pages starting from 4 (as the user mentioned)
course_titles = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[3:]:  # Pages are zero-indexed; start from page 4
        text = page.extract_text()
        if text:
            for line in text.split("\n"):
                if course_pattern.match(line.strip()):  # Match lines that fit the course pattern
                    course_titles.append(line.strip())

# Convert to DataFrame for easy visualization
df_courses = pd.DataFrame(course_titles, columns=["Course Title"])

# Display extracted courses
print("Extracted Course Titles:")
print(df_courses)

# Optionally, save the extracted courses to a CSV file
df_courses.to_csv("data/extracted_courses.csv", index=False)
