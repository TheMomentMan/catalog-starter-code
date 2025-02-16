import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Define paths
pdf_path = "1996.pdf"  # Update with your actual PDF file path
image_folder = "pdf_imagesnew"
os.makedirs(image_folder, exist_ok=True)

# Step 1: Convert PDF pages to images
images = convert_from_path(pdf_path, dpi=300)  # Higher DPI improves OCR accuracy

# Step 2: Extract text from each image and store results
extracted_text_pages = []
for i, image in enumerate(images):
    image_path = os.path.join(image_folder, f"page_{i+1}.png")
    image.save(image_path, "PNG")  # Save image

    # Step 3: Perform OCR (text extraction)
    extracted_text = pytesseract.image_to_string(image, lang="eng")  # Specify language
    extracted_text_pages.append(f"--- Page {i+1} ---\n{extracted_text}\n")

# Step 4: Combine all extracted text
full_extracted_text = "\n".join(extracted_text_pages)

# Step 5: Save extracted text to a file
text_output_path = "extracted_textv5.txt"  # Output text file
with open(text_output_path, "w", encoding="utf-8") as text_file:
    text_file.write(full_extracted_text)

print(f"Text extracted and saved to {text_output_path}")
