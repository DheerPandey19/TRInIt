import fitz 
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import base64
from IPython.display import display, HTML

pdf_url = 'https://jaipur.fiitjee.com/sample%20paper/XII/XII-II.pdf'

response = requests.get(pdf_url)

if response.status_code == 200:
    pdf_file = BytesIO(response.content)
    doc = fitz.open(stream=pdf_file, filetype="pdf")

    questions = []

    for page_num in range(1, len(doc)-1):
        page = doc.load_page(page_num)

        text = page.get_text()

        lines = text.split('\n')

        current_question = ""

        for line in lines:
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.','11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.','21.', '22.', '23.', '24.', '25.', '26.', '27.', '28.', '29.', '30.')):
                if current_question:
                    questions.append(current_question)
                current_question = line
            else:
                current_question += line

        if current_question:
            questions.append(current_question)

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base = img[1]
            img_data = doc.extract_image(xref)
            image_bytes = img_data["image"]

            image = Image.open(BytesIO(image_bytes))

            if questions:
                questions[-1] += f'\nImage {img_index + 1} attached.'

    questions_table = []
    specific_word = "JEE Main Mock Test Paper- " 

    for question in questions:
        if specific_word not in question:
            questions_table.append({"Question": question})

    for q in questions_table:
        print(q)

else:
    print("Failed to download the PDF.")
