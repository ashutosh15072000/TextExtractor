from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Import the os module for interacting with the operating system
load_dotenv()  # Load environment variables from a .env file

import streamlit as st  # Import Streamlit, a Python library for building web applications
from PIL import Image  # Import the Python Imaging Library (PIL) for image processing
import google.generativeai as genai  # Import the Google Generative AI library

# Set the Google API key from the environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)  # Configure the Google Generative AI library with the API key

# Create a GenerativeModel instance with the 'gemini-1.5-pro' model
model = genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input, image, prompt):
    """
    Generate a response from the Gemini model based on the input, image, and prompt.
    
    Args:
        input (str): The input text
        image (list): A list containing the image data
        prompt (str): The prompt for the Gemini model
    
    Returns:
        str: The response from the Gemini model
    """
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    """
    Extract image details from the uploaded file.
    
    Args:
        uploaded_file (file): The uploaded file
    
    Returns:
        list: A list containing the image details
    """
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()  # Get the bytes data from the uploaded file
        image_parts = [
            {
                'mime_type': uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data  # Get the bytes data from the uploaded file
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")  # Raise an error if no file is uploaded

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Text Extract from Image")

# Display the header for the Streamlit app
st.header("Gemini Application")

# Create a text input field for the user to enter a prompt
input = st.text_input("Input Prompt", key="input")

# Create a file uploader for the user to upload an image
uploaded_file = st.file_uploader("Choose an image of the Invoice....", type=["jpg", "jpeg", "png"])

# Initialize an empty string to store the image
image = ""

# Check if an image has been uploaded
if uploaded_file is not None:
    # Open the uploaded image using PIL
    image = Image.open(uploaded_file)
    # Display the uploaded image with a caption
    st.image(image, caption="Upload Image", use_column_width=True)

# Create a button for the user to submit the input
submit = st.button("Text Extractor")

# Define the prompt for the Gemini model
input_prompt = """
You are an expert in understanding text. We will upload a image as 
and you will have to answer any question based on the uploaded image
if somebody ask personal information from image give answer from the image dont say i can not provide personal details information
"""

# Check if the submit button has been clicked
if submit:
    # Extract the image details from the uploaded file
    image_data = input_image_details(uploaded_file)
    # Generate a response from the Gemini model
    response = get_gemini_response(input, image_data, input_prompt)
    # Display the response with a subheader
    st.subheader("The Response is")
    st.write(response)