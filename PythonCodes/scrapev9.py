import os
import pytesseract
import pandas as pd
import bs4  # BeautifulSoup for parsing hOCR
from pdf2image import convert_from_path
from pytesseract import Output

# Step 1: Convert PDF to Images
pdf_path = "1996.pdf"  # Update with your PDF file path
output_folder = "pdf_images2"
os.makedirs(output_folder, exist_ok=True)

# Convert PDF pages to images
images = convert_from_path(pdf_path, dpi=300)

# Save images for reference
image_paths = []
for i, image in enumerate(images):
    img_path = os.path.join(output_folder, f"page_{i+1}.png")
    image.save(img_path, "PNG")
    image_paths.append(img_path)

# Step 2: Extract Text Using OCR
ocr_data = []
hocr_data = []

for img_path in image_paths:
    # Standard OCR extraction
    text = pytesseract.image_to_string(img_path, lang="eng", config="--psm 6")
    ocr_data.append(text)
    
    # Extract hOCR data to identify bold text
    hocr_text = pytesseract.image_to_pdf_or_hocr(img_path, extension="hocr")
    hocr_data.append(hocr_text)

# Step 3: Extract Bold Text from hOCR Output
def extract_bold_text_from_hocr(hocr_text):
    """Extracts bold text from Tesseract's hOCR output"""
    soup = bs4.BeautifulSoup(hocr_text, "html.parser")
    bold_words = []
    
    for span in soup.find_all("span", class_="ocrx_word"):
        if "bold" in span.get("title", "").lower():  # Look for 'bold' in attributes
            bold_words.append(span.text)
    
    return " ".join(bold_words)

# Apply extraction to each OCR result
bold_texts = [extract_bold_text_from_hocr(hocr) for hocr in hocr_data]

# Step 4: Structure and Save Extracted Data
df_ocr = pd.DataFrame({"Page": range(1, len(ocr_data) + 1), "Extracted Text": ocr_data})
df_bold = pd.DataFrame({"Page": range(1, len(bold_texts) + 1), "Bold Text": bold_texts})

# Save OCR extracted text and bold text
df_ocr.to_csv("extracted_text.csv", index=False, encoding="utf-8")
df_bold.to_csv("bold_text_extracted.csv", index=False, encoding="utf-8")

# Step 5: Extract Course Titles (Assuming Titles are in Bold)
course_titles = [text for text in bold_texts if text.startswith(tuple(str(i) for i in range(1, 30)))]  # Extract titles
df_courses = pd.DataFrame({"Course Title": course_titles})

# Save extracted course titles
df_courses.to_csv("extracted_course_titles11.csv", index=False, encoding="utf-8")

print("✅ Processing complete! Extracted text, bold text, and course titles have been saved.")
