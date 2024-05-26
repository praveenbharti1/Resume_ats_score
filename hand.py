from dotenv import load_dotenv

load_dotenv()

import os
import io
import streamlit as st
from PIL import Image
import pdf2image 
import pybase64
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API-KEY"))


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the pdf to Image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # convert to bytes 
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": pybase64.b64encode(img_byte_arr).decode()  # encode to base64

            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    

## Steamlit App
    
st.set_page_config(page_title= "Hand Writting Recognition")
st.header("")
input_text= st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)....", type=["pdf"])

if uploaded_file is not None:
    st.write("Pdf Uploaded Successfully ")

submit1 = st.button("Tell Me About The Resume")


input_prompt1 = """
read all hand written text from the image
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")


