from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
from PIL import Image
import google.generativeai as genai

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


model=genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                'mime_type': uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

st.set_page_config(page_title=" Text Extract from Image ")

st.header("Gemini Application")

input=st.text_input("Input Prompt",key="input")
uploaded_file=st.file_uploader("choose an image of the Invoice....",type=["jpg","jpeg","png"])


image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Upload Image",use_column_width=True)

submit=st.button("Text Extractor")

input_prompt="""
You are an expert in understanding Invoice . We will upload a image as 
invoice and you will have to answer any question based on the uploaded invoice image

"""
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input,image_data,input_prompt)
    st.subheader("The Response is")
    st.write(response)