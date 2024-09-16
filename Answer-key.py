import fitz 
import requests
from io import BytesIO

pdf_url = 'https://jaipur.fiitjee.com/sample%20paper/XII/XII-II.pdf'

response = requests.get(pdf_url)

if response.status_code == 200:
    
    pdf_file = BytesIO(response.content)
    doc = fitz.open(stream=pdf_file, filetype="pdf")

    page = doc.load_page(len(doc)-1)
    text = page.get_text()
    words = text.split()

    answer_key = []
    
    data_capture = False
    subject = ""
    questions_captured = 0

    i = 0
    while i < len(words):
        word = words[i]
        if word.lower() in ["chemistry", "physics", "mathematics"]:
            data_capture = True
            subject = word
            questions_captured = 0 
        elif data_capture and questions_captured < 30:
            if i + 1 < len(words): 
                answer_key.append({"subject": subject, "Question": word, "Answer": words[i + 1]})
                questions_captured += 1 
                i += 2 
                continue 
        elif data_capture and questions_captured >= 30:
            data_capture = False
        
        i += 1 

    for ans in answer_key:
        print(ans)
else:
    print("Failed to download the PDF.")
