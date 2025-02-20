import os

# Folder containing HTML files
folder_path = "/newdata"  # Change this to your folder path
output_file = "combinedhtmls.html"

# Get all HTML files in the folder
html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]

# Sort files (optional, ensures order if numbered)
html_files.sort()

# Combine all HTML content
combined_content = ""

for file in html_files:
    file_path = os.path.join(folder_path, file)
    with open(file_path, "r", encoding="utf-8") as f:
        combined_content += f.read() + "\n"  # Add newline for separation

# Save to a new HTML file
output_path = os.path.join(folder_path, output_file)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(combined_content)

print(f"Combined {len(html_files)} files into {output_file}")
