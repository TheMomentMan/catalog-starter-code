import os
import requests
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Define paths and URLs
pdf_urls = [f"https://onexi.org/catalog/pdf/0{i}.pdf" for i in range(1, 7)]  # 01.pdf to 06.pdf
pdf_folder = "downloaded_pdfs"
image_folder = "pdf_images_combined"
output_text_file = "combined_extracted_text.txt"

# Create necessary directories
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)

# Initialize text storage
extracted_text_pages = []

# Step 1: Download and Process Each PDF
for pdf_url in pdf_urls:
    pdf_name = os.path.basename(pdf_url)
    pdf_path = os.path.join(pdf_folder, pdf_name)

    # Download PDF
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"✅ Downloaded: {pdf_name}")
    else:
        print(f"❌ Failed to download: {pdf_url}")
        continue  # Skip this file if it fails

    # Step 2: Convert PDF to Images
    images = convert_from_path(pdf_path, dpi=300)  # Higher DPI improves OCR accuracy

    # Step 3: Perform OCR and Save Images
    for i, image in enumerate(images):
        image_path = os.path.join(image_folder, f"{pdf_name}_page_{i+1}.png")
        image.save(image_path, "PNG")  # Save image

        # Perform OCR (text extraction)
        extracted_text = pytesseract.image_to_string(image, lang="eng")  # Specify language
        extracted_text_pages.append(f"--- {pdf_name} Page {i+1} ---\n{extracted_text}\n")

# Step 4: Combine all extracted text
full_extracted_text = "\n".join(extracted_text_pages)

# Step 5: Save combined text to a file
with open(output_text_file, "w", encoding="utf-8") as text_file:
    text_file.write(full_extracted_text)

print(f"✅ Combined text extracted and saved to {output_text_file}")
