# combined_ai_suite.py
import streamlit as st 
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# load env and create client (same as original files)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = GEMINI_API_KEY)

# Page config
st.set_page_config(page_title="AI ChatBot Suite", layout="centered")

# Sidebar (small, informational)
st.sidebar.title("AI ChatBot Suite")
st.sidebar.markdown(
    """
**Tools included**
- YouTube Video Summarizer
- Image Caption Generator
- AI Image Generator

**Quick instructions**
1. Add your Gemini API key to a `.env` file as `GEMINI_API_KEY`.
2. Select the tab for the tool you want to use.
3. Enter input and click the relevant button.

**Environment**
- Ensure internet access and a valid Gemini API key.
"""
)

if not GEMINI_API_KEY:
    st.sidebar.error("GEMINI_API_KEY not found in environment. Add it to `.env`.")

# Main title
st.title("AI ChatBot Suite — 📺YouTube Summarizer | 🖼️ Image Caption | 🎨 Image Generator")

# Create tabs for the three apps
tab1, tab2, tab3 = st.tabs(["📺 YouTube Video Summarizer", "🖼️ Image Caption Generator", "🎨 AI Image Generator"])

# --------------------------
# Tab 1: YouTube Video Summarizer
# --------------------------
with tab1:
    st.header("AI YouTube Video Summarizer")
    # Use unique keys to avoid collisions when used in single app
    youtube_url = st.text_input("Enter Youtube Video URL", key="youtube_url_input")

    if st.button("Summarize Video", key="summarize_btn"):
        if not youtube_url:
            st.warning("No youtube URL present!")
        else:
            try:
                with st.spinner("Generating summary.....!!!"):
                    response = client.models.generate_content(
                        model='models/gemini-2.0-flash',
                        contents=types.Content(
                            parts = [
                                types.Part(text = "Summarize the video, keep it brief and concise, focusing on important points and concepts. Bullet these points."),
                                types.Part(
                                    file_data=types.FileData(file_uri= youtube_url)
                                )
                            ]  
                        )
                    )
                st.subheader("Video Summary")
                st.write(response.text)
            except Exception as e:
                st.error("Error Generating Summary")
                st.error(str(e))

# --------------------------
# Tab 2: Image Caption Generator
# --------------------------
with tab2:
    st.header("AI Image Caption Generator")
    uploaded_image = st.file_uploader("Upload an image for caption generation", type = ["png", "jpg", "jpeg"], key="caption_uploader")

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate Caption", key="generate_caption_btn"):
            try:
                with st.spinner("Generating Caption.....!!!"):
                    # Keep the original call signature / core logic
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=["Generate a creative caption for the image", image])
                    st.subheader("Generated Caption: ")
                    st.write(response.text)
                        
            except Exception as e:
                st.error("Error Generating Caption")
                st.error(str(e))

# --------------------------
# Tab 3: AI Image Generator
# --------------------------
with tab3:
    st.header("AI Image Generator")
    user_prompt = st.text_input("What do you want to generate image for?", key="image_prompt_input")

    if st.button("Generate Image", key="generate_image_btn"):
        if not user_prompt:
            st.warning("Please enter the prompt!")
        else:
            try:
                with st.spinner("Generating image....!"):
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-exp-image-generation",
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["Text", "Image"]
                        )
                    )

                st.subheader("Generated Image")
                # original logic: iterate through response candidates and show text and inline images
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write(part.text)
                    elif part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, use_column_width=True)

            except Exception as e:
                st.error("Error Generating Image")
                st.error(str(e))
