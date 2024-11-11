import streamlit as st
import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress
from transformers import pipeline
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

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

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    match = re.search(r"v=([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None

def get_transcript_from_api(video_id):
    """Get transcript using YouTube Transcript API."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for segment in transcript:
            transcript_text += segment["text"] + " "
        return transcript_text
    except Exception as e:
        st.error(f"Error getting transcript from YouTube API: {str(e)}")
        return None

def get_audio_and_transcribe(url):
    """Get audio and transcribe using pytubefix and whisper."""
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio_stream = yt.streams.get_audio_only()
        out_file = audio_stream.download(mp3=True)
        
        with st.spinner('Transcribing audio...'):
            result = model.transcribe(out_file)
            os.remove(out_file)
            return result['text']
    except Exception as e:
        st.warning(f"pytubefix method failed: {str(e)}")
        return None

def get_text(url):
    """Get text using either pytubefix+whisper or YouTube Transcript API."""
    # First try pytubefix + whisper method
    transcript = get_audio_and_transcribe(url)
    
    # If pytubefix method fails, try YouTube Transcript API
    if transcript is None:
        st.info("Trying alternative method using YouTube Transcript API...")
        video_id = extract_video_id(url)
        if video_id:
            transcript = get_transcript_from_api(video_id)
        else:
            st.error("Invalid YouTube URL")
            return None
    
    return transcript

def get_summary(text):
    try:
        if text:
            with st.spinner('Generating summary...'):
                # Split text into chunks of 1000 characters
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

st.info("""
    This app will first try to download and transcribe the audio directly. 
    If that fails, it will automatically try to fetch the transcript from YouTube's API.
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
