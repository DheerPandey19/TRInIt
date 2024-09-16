import fitz 
import requests
from io import BytesIO

pdf_url = 'https://jaipur.fiitjee.com/sample%20paper/XII/XII-I.pdf'

response = requests.get(pdf_url)

if response.status_code == 200:
  
    pdf_file = BytesIO(response.content)
    doc = fitz.open(stream=pdf_file, filetype="pdf")

    extracted_text = ""

    for page in doc:
        text = page.get_text()
        extracted_text += text

    print(extracted_text)
else:
    print("Failed to download the PDF.")
