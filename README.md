# YouTube Video Transcriber and Summarizer

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-yellow)

A Streamlit web application that transcribes YouTube videos and generates summaries using OpenAI's Whisper model and Hugging Face's transformers. The app provides dual methods for transcription: direct audio processing with Whisper and `youtube-transcript-api`.

## 📋 Features

- **Dual Transcription Methods**:
  - Primary: OpenAI's Whisper model for audio transcription
  - Fallback: `youtube-transcript-api`
- **Text Summarization**: Generate concise summaries using Hugging Face transformers
- **Clean Interface**: User-friendly UI built with Streamlit
- **Error Handling**: Automatic fallback system if primary method fails
- **Progress Tracking**: Real-time status updates during processing

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/rajeshai/Youtube-Transcription.git
cd Youtube-Transcription
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

5. Open your browser and go to `http://localhost:8501`

## 📦 Requirements

Create a `requirements.txt` file with these dependencies:
```text
streamlit
openai-whisper
pytubefix
transformers
torch
youtube_transcript_api
```

## 💻 Usage

1. Launch the application
2. Enter a YouTube URL in either the Transcription or Summary tab
3. Click the respective button to get either:
   - Full video transcription
   - Summarized content

## 🔧 How It Works

1. **Transcription Process**:
   - First attempts to download audio using `pytubefix` and transcribe with Whisper
   - If that fails, automatically switches to `youtube-transcript-api`
   - Shows clear status messages throughout the process

2. **Summarization Process**:
   - Processes transcribed text using Hugging Face's summarization pipeline
   - Handles long transcripts by chunking text into manageable segments
   - Combines summaries for a coherent final output

## ⚠️ Known Limitations

- YouTube may occasionally block `pytubefix` and `youtube-transcript-api` requests
- Some videos might not have available transcripts through YouTube's API
- Processing long videos may take additional time
- Summarization quality depends on transcript accuracy

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for audio transcription
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) for text summarization
- [Streamlit](https://streamlit.io/) for the web interface
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for the fallback transcription method


---

**Note**: Please ensure you comply with YouTube's terms of service when using this application.
