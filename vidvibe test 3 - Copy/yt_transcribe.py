try:
    from youtube_transcript_api._api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
except ImportError:
    raise ImportError("youtube_transcript_api is not installed. Please run 'pip install youtube-transcript-api'.")
import os
from dotenv import load_dotenv
from generate_audio import generate_summary_audio
load_dotenv()

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    import re
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})",
        r"youtube\.com/watch\?v=([\w-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

def transcribe_from_url(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL. Could not extract video ID.")
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in transcript_list])
        
        # Get absolute path for transcript file
        transcript_path = os.path.abspath("transcript.txt")
        print(f"Saving transcript to: {transcript_path}")
        
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        # Verify file was created successfully
        if os.path.exists(transcript_path):
            file_size = os.path.getsize(transcript_path)
            print(f"Transcript saved successfully. File size: {file_size} bytes")
        else:
            print(f"Warning: Transcript file was not created at {transcript_path}")
        
        return transcript
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise RuntimeError("No transcript found for this video.")
    except VideoUnavailable:
        raise RuntimeError("The video is unavailable.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transcript: {str(e)}")

def summarize_transcript(transcript):
    import openai
   
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"""
    Summarize the following transcript into 5 simple beginner-friendly bullet points:
    {transcript[:2000]}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        
        # Generate audio from the summary
        try:
            generate_summary_audio(summary)
            print("Audio file generated successfully from summary")
        except Exception as audio_error:
            print(f"Warning: Failed to generate audio: {str(audio_error)}")
        
        return summary
    except Exception as e:
        return f"❌ Failed to generate summary: {str(e)}"