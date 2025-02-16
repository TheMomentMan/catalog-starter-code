import re
import pandas as pd
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup

# Step 1: Convert PDF to HTML
pdf_path = "1996.pdf"
html_output_path = "data/converted_1996.html"

# Extract text from the PDF
extracted_text = extract_text(pdf_path)

# Convert extracted text into structured HTML with paragraph and break tags
html_body = ""
for line in extracted_text.split("\n"):
    line = line.strip()
    if line:
        html_body += f"<p>{line}</p>\n"

# Wrap in full HTML structure
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted PDF</title>
</head>
<body>
{html_body}
</body>
</html>
"""

# Save the HTML file
with open(html_output_path, "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

# Step 2: Extract Course Titles from the HTML

# Read the formatted HTML file
with open(html_output_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Extract all text from the HTML body
text_lines = [line.strip() for line in soup.body.stripped_strings]

# Improved regex pattern to match course titles (e.g., "1.00", "1.251J", etc.)
course_pattern = re.compile(r"^\d+\.\d+[A-Za-z]*\s+.+")  

course_titles = []
current_title = ""

for line in text_lines:
    line = line.strip()

    # Identify a new course title if it matches the regex pattern
    if course_pattern.match(line):
        if current_title:
            course_titles.append(current_title.strip())  # Save the previous title
        current_title = line  # Start a new title
    elif current_title and (line.lower().startswith("prereq") or line.startswith("(")):
        course_titles.append(current_title.strip())  # Save last title before prerequisites
        current_title = ""
    elif current_title:
        current_title += " " + line  # Continue building multi-line titles

# Ensure the last captured title is added
if current_title:
    course_titles.append(current_title.strip())

# Convert to DataFrame
df_courses = pd.DataFrame(course_titles, columns=["Course Title"])

# Export DataFrame to CSV
csv_output_path = "data/extracted_course_titles4.csv"
df_courses.to_csv(csv_output_path, index=False, encoding="utf-8")

# Display the extracted courses table
import pandas as pd
print("Extracted Course Titles:")
print(df_courses)

# Provide the CSV file path for downloading
#df_courses.to_csv("data/extracted_courses4.csv", index=False)
