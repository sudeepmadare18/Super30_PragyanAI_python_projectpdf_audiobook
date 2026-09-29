import os
import streamlit as st
import PyPDF2

from gtts import gTTS
from langdetect import detect


st.set_page_config(
    page_title="PDF to Audiobook",
    page_icon="📖",
    layout="centered"
)

st.title("📖 PDF to Audiobook 🎧")
st.write("Upload a PDF book and convert it into an audiobook.")


def pdf_to_audiobook(pdf_file):

    # Save uploaded PDF temporarily
    pdf_path = "/tmp/input.pdf"

    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    # Extract text
    full_text = ""

    with open(pdf_path, "rb") as file:

        pdf_reader = PyPDF2.PdfReader(file)

        total_pages = len(pdf_reader.pages)

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                full_text += text + "\n"

    if not full_text.strip():
        return None, total_pages, None

    # Detect language
    language = detect(full_text[:5000])

    supported_languages = {
        "en": "en",
        "hi": "hi",
        "mr": "mr",
        "fr": "fr",
        "de": "de",
        "es": "es",
        "it": "it",
        "pt": "pt",
        "ru": "ru",
        "ja": "ja",
        "ko": "ko",
        "zh-cn": "zh-CN"
    }

    if language not in supported_languages:
        language = "en"

    # Create audiobook
    output_file = "/tmp/audiobook.mp3"

    tts = gTTS(
        text=full_text,
        lang=supported_languages[language],
        slow=False
    )

    tts.save(output_file)

    return output_file, total_pages, language


uploaded_file = st.file_uploader(
    "📄 Upload your PDF book",
    type=["pdf"]
)


if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🎧 Convert to Audiobook"):

        with st.spinner("Creating your audiobook... Please wait."):

            try:

                audio_file, pages, language = pdf_to_audiobook(
                    uploaded_file
                )

                if audio_file is None:

                    st.error(
                        "❌ No readable text found. "
                        "This may be a scanned PDF."
                    )

                else:

                    st.success("✅ Audiobook created successfully!")

                    st.write(f"📄 Pages: {pages}")
                    st.write(f"🌐 Detected language: {language}")

                    # Audio player
                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()

                    st.audio(audio_bytes, format="audio/mp3")

                    # Download button
                    st.download_button(
                        label="⬇️ Download Audiobook",
                        data=audio_bytes,
                        file_name="audiobook.mp3",
                        mime="audio/mpeg"
                    )

            except Exception as e:

                st.error(f"❌ Error: {e}")
