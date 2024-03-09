import fitz # PyMuPDF
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import base64
from IPython.display import display, HTML

# URL of the PDF
pdf_url = 'https://jaipur.fiitjee.com/sample%20paper/XII/XII-II.pdf'

# Download the PDF
response = requests.get(pdf_url)

# Check if the request was successful
if response.status_code == 200:
    # Open the PDF from the response content
    pdf_file = BytesIO(response.content)
    doc = fitz.open(stream=pdf_file, filetype="pdf")

    # Initialize an empty string to hold the HTML content
    html_content = "<html><body>"
    
    questions=[]

    # Iterate over each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text from the page
        text = page.get_text()

        lines=text.split('\n')

        current_question=""

        for line in lines:
            # Implement your heuristic to identify questions here
            # For example, if questions start with a number followed by a period:
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.','11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.','21.', '22.', '23.', '24.', '25.', '26.', '27.', '28.', '29.', '30.')):
                # If there's a current question, add it to the list of questions
                if current_question:
                    questions.append(current_question)
                # Start a new question
                current_question = line
            else:
                # Add the line to the current question
                current_question += "\n" + line

        # Add the last question to the list of questions
        if current_question:
            questions.append(current_question)

        # Extract images from the page
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base = img[1]
            img_data = doc.extract_image(xref)
            image_bytes = img_data["image"]

            # Convert the image bytes to a PIL Image
            image = Image.open(BytesIO(image_bytes))

            # Convert the image to base64 for embedding in HTML
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            # Add the image to the last question in the list
            if questions:
                questions[-1] += f'<img src="data:image/png;base64,{image_base64}" />'
    
    for question in questions:
        html_content += f"<p>{question}</p>"

    # Close the HTML content
    html_content += "</body></html>"

    # Save the HTML content to a file
    with open("output.html", "w") as html_file:
        html_file.write(html_content)
    # Assuming the HTML file is named 'output.html' and is in the current working directory
    with open('output.html', 'r') as file:
        html_content = file.read()

    # Display the HTML content
    display(HTML(html_content))
   
else:
    print("Failed to download the PDF.")

from google.colab import files

files.download('output.html')
