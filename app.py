import streamlit as st
import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress
from transformers import pipeline
import os

# Set page configuration
st.set_page_config(
    page_title="YouTube Video Transcription & Summarization",
    page_icon="🎥",
    layout="wide"
)

# Initialize models
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    summarizer = pipeline("summarization")
    return whisper_model, summarizer

model, summarizer = load_models()

def get_audio(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio_stream = yt.streams.get_audio_only()
        out_file = audio_stream.download(mp3=True)
        return out_file
    except Exception as e:
        st.error(f"Error downloading audio: {str(e)}")
        return None

def get_text(url):
    try:
        audio_file = get_audio(url)
        if audio_file:
            with st.spinner('Transcribing audio...'):
                result = model.transcribe(audio_file)
                # Clean up the downloaded file
                os.remove(audio_file)
                return result['text']
        return None
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def get_summary(text):
    try:
        if text:
            with st.spinner('Generating summary...'):
                chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
                summaries = []
                for chunk in chunks:
                    summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                    summaries.append(summary[0]['summary_text'])
                return " ".join(summaries)
        return None
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

# App UI
st.title("YouTube Video Transcription & Summarization")
st.markdown("Enter the link of any YouTube video to get its transcription and summary.")

st.warning("""
    Note: This app uses the pytubefix library to fetch audio from YouTube URLs. 
    If YouTube is blocking requests, you might experience errors.
""")

# Create tabs
tab1, tab2 = st.tabs(["Transcription", "Summary"])

with tab1:
    st.header("Get Video Transcription")
    url_input_1 = st.text_input("Enter YouTube URL", key="url1", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Get Transcription", key="transcribe_btn"):
        if url_input_1:
            transcription = get_text(url_input_1)
            if transcription:
                st.success("Transcription completed!")
                st.text_area("Transcription", transcription, height=300)
        else:
            st.error("Please enter a valid YouTube URL")

with tab2:
    st.header("Get Video Summary")
    url_input_2 = st.text_input("Enter YouTube URL", key="url2", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Get Summary", key="summary_btn"):
        if url_input_2:
            transcription = get_text(url_input_2)
            if transcription:
                summary = get_summary(transcription)
                if summary:
                    st.success("Summary generated!")
                    st.text_area("Summary", summary, height=200)
        else:
            st.error("Please enter a valid YouTube URL")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit, OpenAI Whisper, and Hugging Face Transformers")
