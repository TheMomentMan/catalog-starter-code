import re
import pandas as pd

# Load the extracted text file
file_path = "combined_extracted_text.txt"  # Update with actual file path
with open(file_path, "r", encoding="utf-8") as file:
    text_lines = file.readlines()

# Define regex pattern for course codes (e.g., "1.00", "18.014", "1.124J", "1.691", "8.981, 8.982")
course_pattern = re.compile(r"(\b\d+\.\d+[A-Za-z]*\b(?:, \d+\.\d+[A-Za-z]*)*)")  # Handles multiple course codes

course_titles = []
current_title = ""
pending_codes = []  # Stores course codes when a title spans multiple lines

for line in text_lines:
    line = line.strip()

    # Identify course codes at the beginning of a line
    match = course_pattern.match(line)

    if match:
        codes = match.group(1).split(", ")  # Split multiple course codes
        title_start = match.end()  # Get the rest of the line after the course code(s)
        title_text = line[title_start:].strip()

        if title_text:
            # Store each code with the title in one continuous stretch
            for code in codes:
                course_titles.append(f"{code} {title_text}")
        else:
            # If the title is on the next line, store course codes and wait for the next line
            pending_codes = codes
            current_title = ""

    elif pending_codes:
        # Continue a multi-line title unless it starts with "Prereq" or contains "("
        if line.lower().startswith("prereq") or "(" in line:
            for code in pending_codes:
                course_titles.append(f"{code} {current_title.strip()}")
            pending_codes = []
            current_title = ""
        else:
            current_title += " " + line  # Append continued title

# Ensure the last captured title is added
if pending_codes and current_title:
    for code in pending_codes:
        course_titles.append(f"{code} {current_title.strip()}")

# Convert to DataFrame
df_courses = pd.DataFrame({"Course Title": course_titles})

# Save the extracted course titles to CSV
csv_output_path = "titlescourse.csv"
df_courses.to_csv(csv_output_path, index=False, encoding="utf-8")

# Display extracted course titles
print("✅ Extracted course titles successfully!")
print(df_courses.head(20))  # Display first 20 extracted titles

print(f"✅ Extracted course titles saved to {csv_output_path}")
