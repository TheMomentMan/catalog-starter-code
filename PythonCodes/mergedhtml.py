import glob

# Define folder and output file
folder = "data/"
output_file = "merged.html"

# Get all HTML files in the folder
html_files = glob.glob(folder + "*.html")

# Merge all HTML files into one
with open(output_file, "w", encoding="utf-8") as outfile:
    for file in html_files:
        with open(file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read() + "\n")  # Read and append content with a newline

print(f"Merged {len(html_files)} HTML files into {output_file}")
