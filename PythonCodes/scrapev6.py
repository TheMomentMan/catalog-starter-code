from pdf2image import convert_from_path
import pytesseract

# Convert PDF to images
pages = convert_from_path('1996.pdf', 300)

# Extract text from the first page
first_page_text = pytesseract.image_to_string(pages[3])
print(first_page_text)