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
    
st.set_page_config(page_title= "ATS Resume Expert")
st.header("ATS Tracker System")
input_text= st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)....", type=["pdf"])

if uploaded_file is not None:
    st.write("Pdf Uploaded Successfully ")

submit1 = st.button("Tell Me About The Resume")

submit2 = st.button("How Can I Improve My Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
you are an experienced HR with Tech Experince in the field of any one job role Data Science, 
Full Stack Web Development, Big Data Enginering, DevOps, Data Analyst, 
your task is to review the provided resume against the job description for these profiles.
please share your proffessional evaluation on weather the candidate's profile 
align with the role. Highlight the strength and weakness of the applicant in 
relation to the specified Job Description.
"""

input_prompt3 = """"
 you are an skilled ATS (Applicant Tracking System) scanner with a 
 deep understanding of any one of job role  Data Science, Full Stack web development, Big Data Engineering,
 DevOps, Data Analyst and deep ATS functionality, your task is to evaluate 
 the resume against the provided job descriptio, give me the percentage of
 match if the resume matches the job description. 
 First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
