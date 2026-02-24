import streamlit as st
from PIL import Image
import google.generativeai as genai
import io
import os


# ---------------------------
# Function to setup input image
# ---------------------------
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# ---------------------------
# Streamlit App Config
# ---------------------------
st.set_page_config(
    page_title="Gemini Historical Artifact Description App", page_icon="🏺"
)

st.header("🏺 Gemini Historical Artifact Description App")

# Google Gemini API key setup
api_key = st.text_input("🔑 Enter your Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Google API Key to continue.")
    st.stop()

# ---------------------------
# Input section
# ---------------------------
input_text = st.text_input("💬 Input Prompt:", key="input")
uploaded_file = st.file_uploader(
    "🖼️ Choose an image of an artifact...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

submit = st.button("🚀 Generate Artifact Description")

# ---------------------------
# Default historian prompt
# ---------------------------
input_prompt = """
You are a historian. Please describe the historical artifact in the image and provide detailed
information, including its name, origin, time period, and historical significance.
"""

# ---------------------------
# On submit
# ---------------------------
if submit:
    try:
        image_data = input_image_setup(uploaded_file)

        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([input_text, image_data, input_prompt])

        st.subheader("📜 Description of the Artifact:")
        st.write(response.text)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
