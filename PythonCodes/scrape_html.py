import os
from pdf2image import convert_from_path
import pytesseract

# Define paths
pdf_path = "1996.pdf"  # Update with your actual PDF file path
image_folder = "pdf_imagesnew"
output_html_path = "extracted_ocr_output.html"
os.makedirs(image_folder, exist_ok=True)

# Step 1: Convert PDF pages to images
poppler_path = '/home/linuxbrew/.linuxbrew/bin/'  # Update with the actual path to the Poppler bin directory
images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)  # Higher DPI improves OCR accuracy

# Step 2: Perform OCR on each image and store hOCR output
ocr_output = ""
for i, image in enumerate(images):
    hocr = pytesseract.image_to_pdf_or_hocr(image, extension="hocr")
    ocr_output += hocr.decode('utf-8')

# Step 3: Save the OCR-processed HTML output
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(ocr_output)

print(f"✅ OCR HTML output saved as: {output_html_path}")