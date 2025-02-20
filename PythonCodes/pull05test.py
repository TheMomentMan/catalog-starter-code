import json

# Load the cleaned JSON file
cleaned_file = "cleaned_courses.json"
with open(cleaned_file, "r", encoding="utf-8") as file:
    cleaned_courses = json.load(file)

# Extract course titles
course_titles = [course["title"] for course in cleaned_courses if "title" in course]

# Save extracted course titles to a text file
output_file = "course_titles.txt"
with open(output_file, "w", encoding="utf-8") as file:
    for title in course_titles:
        file.write(title + "\n")

print(f"Course titles extracted and saved to {output_file}")
