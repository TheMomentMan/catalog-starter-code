from bs4 import BeautifulSoup

# Sample HTML content (you can read from a file instead)
with open("merged.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extract all text within <strong> tags
strong_texts = [tag.get_text() for tag in soup.find_all("strong")]

# Print results
for text in strong_texts:
    print(text)
